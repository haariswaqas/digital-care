from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets, status
from ..models import HealthCard
from ..serializers import HealthCardSerializer



class HealthCardViewSet(viewsets.ModelViewSet):
    queryset = HealthCard.objects.all()
    serializer_class = HealthCardSerializer

    @action(detail=True, methods=["post"])
    def link_nhis(self, request, pk=None):
        """User submits NHIS number to link their card"""
        card = self.get_object()
        nhis_number = request.data.get("nhis_number")

        if not nhis_number:
            return Response({"error": "NHIS number is required"}, status=status.HTTP_400_BAD_REQUEST)

        # Start verification process (simulated for now)
        if card.initiate_nhis_verification(nhis_number):
            # Demo: auto-complete verification as successful
            card.complete_nhis_verification(success=True, verification_data={"source": "mock"})
            return Response({"message": "NHIS linked successfully", "card": HealthCardSerializer(card).data})

        return Response({"error": "Unable to link NHIS card"}, status=status.HTTP_400_BAD_REQUEST)
