# api/models/health_card.py
import io
import json
import uuid
from datetime import timedelta
from typing import Optional, Dict, Any
from api.utils import default_expiry
from django.conf import settings
from django.core.files.base import ContentFile
from django.db import models
from django.utils import timezone
from django.utils.crypto import get_random_string
from django.contrib.auth.hashers import make_password, check_password
from django.core.exceptions import ValidationError

import qrcode

from ..authentication_models import User



class HealthCard(models.Model):
    class CardType(models.TextChoices):
        SMART = "smart", "Smart Health Card"
        NHIS = "nhis", "NHIS Card (Linked)"
        HYBRID = "hybrid", "Smart Card with NHIS Link"  # New option

    class Status(models.TextChoices):
        ACTIVE = "active", "Active"
        REVOKED = "revoked", "Revoked"
        EXPIRED = "expired", "Expired"
        PENDING_VERIFICATION = "pending", "Pending NHIS Verification"

    class NHISLinkStatus(models.TextChoices):
        NOT_LINKED = "not_linked", "Not Linked to NHIS"
        PENDING = "pending", "NHIS Verification Pending"
        VERIFIED = "verified", "NHIS Verified and Linked"
        FAILED = "failed", "NHIS Verification Failed"
        EXPIRED = "expired", "NHIS Link Expired"

   
    
    # Keep UUID for external references and QR tokens if needed
    external_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True,
                                   help_text="UUID for external API references and QR codes")
    
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="health_card"
    )

    # Enhanced NHIS Integration
    card_type = models.CharField(
        max_length=10, choices=CardType.choices, default=CardType.SMART
    )
    
    # NHIS Integration Fields
    nhis_number = models.CharField(
        max_length=20, blank=True, null=True, 
        help_text="NHIS card number for linking",
        db_index=True  # For faster lookups
    )
    nhis_link_status = models.CharField(
        max_length=15, choices=NHISLinkStatus.choices, 
        default=NHISLinkStatus.NOT_LINKED
    )
    nhis_verified_at = models.DateTimeField(
        null=True, blank=True,
        help_text="When NHIS linking was last verified"
    )
    nhis_verification_attempts = models.PositiveIntegerField(
        default=0,
        help_text="Number of NHIS verification attempts"
    )
    nhis_last_sync = models.DateTimeField(
        null=True, blank=True,
        help_text="Last successful data sync with NHIS"
    )
    
    # Store NHIS verification data (encrypted in production)
    nhis_verification_data = models.JSONField(
        null=True, blank=True,
        help_text="Encrypted NHIS verification details"
    )

    # Identification
    card_number = models.CharField(
        max_length=32, unique=True, editable=False,
        help_text="Human-readable card number (e.g. SMART-XXXX-XXXX)"
    )
    nfc_uid = models.CharField(
        max_length=64, blank=True, null=True,
        help_text="If a physical NFC card exists, store its chip UID here"
    )

    # Access control
    pin_hash = models.CharField(
        max_length=128, blank=True, null=True,
        help_text="Hashed PIN (optional, for in-person verification)"
    )

    # QR / token - use external_id instead of separate token
    qr_image = models.ImageField(
        upload_to="qr/health_cards/", blank=True, null=True
    )

    # Lifecycle
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.ACTIVE
    )
    issued_at = models.DateTimeField(default=timezone.now)
    expires_at = models.DateTimeField(default=default_expiry())

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['nhis_number', 'nhis_link_status']),
            models.Index(fields=['external_id']),
            models.Index(fields=['card_number']),
        ]

    def __str__(self):
        nhis_info = f" (NHIS: {self.nhis_number})" if self.nhis_number else ""
        return f"{self.get_card_type_display()} · {self.card_number}{nhis_info} · {self.user.email}"

    def clean(self):
        """Model validation"""
        super().clean()
        
        # Validate NHIS number format if provided
        if self.nhis_number and not self._is_valid_nhis_format(self.nhis_number):
            raise ValidationError({
                'nhis_number': 'Invalid NHIS number format'
            })
        
        # Validate card type and NHIS linking consistency
        if self.card_type in [self.CardType.NHIS, self.CardType.HYBRID]:
            if not self.nhis_number:
                raise ValidationError({
                    'nhis_number': 'NHIS number required for NHIS-linked cards'
                })

    @staticmethod
    def _is_valid_nhis_format(nhis_number: str) -> bool:
        """
        Validate NHIS number format - adjust based on actual NHIS format
        This is a placeholder - implement actual NHIS validation
        """
        import re
        # Example: assuming NHIS numbers are 10-15 digits
        pattern = r'^\d{10,15}$'
        return bool(re.match(pattern, nhis_number.strip()))

    # PIN helpers
    def set_pin(self, raw_pin: str):
        """Store a hashed PIN."""
        self.pin_hash = make_password(raw_pin)

    def check_pin(self, raw_pin: str) -> bool:
        if not self.pin_hash:
            return False
        return check_password(raw_pin, self.pin_hash)

    # NHIS Integration Methods
    def can_link_nhis(self) -> bool:
        """Check if card can be linked to NHIS"""
        return (
            self.card_type in [self.CardType.NHIS, self.CardType.HYBRID] and
            self.nhis_link_status in [self.NHISLinkStatus.NOT_LINKED, self.NHISLinkStatus.FAILED] and
            self.nhis_verification_attempts < 3
        )

    def initiate_nhis_verification(self, nhis_number: str) -> bool:
        """
        Start NHIS verification process
        Returns True if verification was initiated
        """
        if not self.can_link_nhis():
            return False
        
        self.nhis_number = nhis_number
        self.nhis_link_status = self.NHISLinkStatus.PENDING
        self.nhis_verification_attempts += 1
        self.save(update_fields=['nhis_number', 'nhis_link_status', 'nhis_verification_attempts'])
        
        # TODO: Trigger async task to verify with NHIS API
        # from .tasks import verify_nhis_card
        # verify_nhis_card.delay(self.id)
        
        return True

    def complete_nhis_verification(self, success: bool, verification_data: Optional[Dict] = None):
        """Mark NHIS verification as complete"""
        if success:
            self.nhis_link_status = self.NHISLinkStatus.VERIFIED
            self.nhis_verified_at = timezone.now()
            self.nhis_verification_data = verification_data or {}
            
            # Update card type to hybrid if it was just smart
            if self.card_type == self.CardType.SMART:
                self.card_type = self.CardType.HYBRID
        else:
            self.nhis_link_status = self.NHISLinkStatus.FAILED
        
        self.save(update_fields=[
            'nhis_link_status', 'nhis_verified_at', 
            'nhis_verification_data', 'card_type'
        ])

    def sync_with_nhis(self) -> bool:
        """
        Sync card data with NHIS system
        Returns True if sync was successful
        """
        if self.nhis_link_status != self.NHISLinkStatus.VERIFIED:
            return False
        
        # TODO: Implement NHIS API sync
        # success = nhis_api_client.sync_patient_data(self.nhis_number)
        # if success:
        #     self.nhis_last_sync = timezone.now()
        #     self.save(update_fields=['nhis_last_sync'])
        
        return True

    def is_nhis_link_valid(self) -> bool:
        """Check if NHIS link is still valid"""
        if self.nhis_link_status != self.NHISLinkStatus.VERIFIED:
            return False
        
        # Check if verification is not too old (e.g., 6 months)
        if self.nhis_verified_at:
            six_months_ago = timezone.now() - timedelta(days=180)
            return self.nhis_verified_at > six_months_ago
        
        return False

    # QR helpers
    def qr_payload(self) -> str:
        """Generate QR payload using external_id instead of separate token"""
        payload = {
            "v": 2,                           # Updated version
            "type": self.card_type,
            "id": str(self.external_id),      # Use UUID for external references
            "nhis": bool(self.nhis_number and self.nhis_link_status == self.NHISLinkStatus.VERIFIED)
        }
        return json.dumps(payload, separators=(",", ":"))

    def build_qr_image(self):
        """Generate QR image from payload"""
        img = qrcode.make(self.qr_payload())
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        filename = f"card_{self.external_id}.png"
        self.qr_image.save(filename, ContentFile(buf.getvalue()), save=False)

    # Card number generation
    @staticmethod
    def _generate_card_number(prefix="SMART"):
        part1 = get_random_string(4, allowed_chars="ABCDEFGHJKLMNPQRSTUVWXYZ23456789")
        part2 = get_random_string(4, allowed_chars="ABCDEFGHJKLMNPQRSTUVWXYZ23456789")
        return f"{prefix}-{part1}-{part2}"

    def save(self, *args, **kwargs):
        # Auto-generate card number if needed
        if not self.card_number:
            if self.card_type == self.CardType.NHIS:
                prefix = "NHIS"
            elif self.card_type == self.CardType.HYBRID:
                prefix = "HYBRID"
            else:
                prefix = "SMART"
            
            cn = self._generate_card_number(prefix=prefix)
            while HealthCard.objects.filter(card_number=cn).exists():
                cn = self._generate_card_number(prefix=prefix)
            self.card_number = cn

        super().save(*args, **kwargs)
        
        # Build QR if missing
        if not self.qr_image:
            self.build_qr_image()
            super().save(update_fields=["qr_image"])