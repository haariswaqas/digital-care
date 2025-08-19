from rest_framework import generics, status
from rest_framework.response import Response
from ..serializers import PasswordResetConfirmSerializer, PasswordResetRequestSerializer
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from ..models import User
from ..tasks import send_email_task



class PasswordResetRequestView(generics.GenericAPIView):
    serializer_class = PasswordResetRequestSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        user = User.objects.get(email=email)
        token = PasswordResetTokenGenerator().make_token(user)
        uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
        
        reset_link = request.build_absolute_uri(
            f"http://localhost:5174/auth/password-reset-confirm?uidb64={uidb64}&token={token}"
        )

        subject = "Password Reset Request"
        message = (
            f"Hi {user.username},\n\n"
            "You requested a password reset. Click the link below to reset your password:\n\n"
            f"{reset_link}\n\n"
            "If you did not request this, please ignore this email.\n\n"
            "Best regards,\nHospital Admin"
        )
        send_email_task.delay(subject, message, [user.email])
        return Response({"detail": "Password reset email sent."}, status=status.HTTP_200_OK)
        


class PasswordResetConfirmView(generics.GenericAPIView):
    serializer_class = PasswordResetConfirmSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        serializer.save()

        subject = "Your Password Has Been Reset Successfully"
        message = (
            f"Hi {user.username},\n\n"
            "Your password has been reset successfully. If you did not initiate this change, please contact support immediately.\n\n"
            "Best regards,\nHospital Admin"
        )
        send_email_task.delay(subject, message, [user.email])
        return Response({"detail": "Password has been reset successfully."}, status=status.HTTP_200_OK)
