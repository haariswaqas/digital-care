# api/views/facility_views.py

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from ..models import Facility
from ..serializers import FacilitySerializer
from ..permissions import IsFacilityAdminOfOwnFacility
from math import radians, cos, sin, asin, sqrt

class FacilityViewSet(viewsets.ModelViewSet):
    queryset = Facility.objects.all()
    serializer_class = FacilitySerializer
    permission_classes = [IsAuthenticated, IsFacilityAdminOfOwnFacility]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser or user.role == 'admin':
            return Facility.objects.all()
        elif user.role == 'facility_admin':
            # facility admin can only see their facility
            return Facility.objects.filter(admin=user)
        return Facility.objects.none()

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def nearby(self, request):
        user = request.user

        # Determine patient's profile latitude and longitude
        profile = None
        if user.role == "adult" and hasattr(user, "adultprofile"):
            profile = user.adultprofile
        elif user.role == "student" and hasattr(user, "studentprofile"):
            profile = user.studentprofile
        elif user.role == "visitor" and hasattr(user, "visitorprofile"):
            profile = user.visitorprofile

        if not profile or profile.latitude is None or profile.longitude is None:
            return Response({"detail": "Patient location not set."}, status=400)

        user_lat = profile.latitude
        user_lon = profile.longitude
        radius_km = float(request.query_params.get("radius", 10))  # default 10 km

        def haversine(lat1, lon1, lat2, lon2):
            # convert decimal degrees to radians
            lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
            # haversine formula
            dlat = lat2 - lat1
            dlon = lon2 - lon1
            a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
            c = 2 * asin(sqrt(a))
            km = 6371 * c
            return km

        nearby_facilities = []
        for facility in Facility.objects.filter(facility_type='clinic', status='Approved'):
            if facility.latitude is None or facility.longitude is None:
                continue
            distance = haversine(user_lat, user_lon, facility.latitude, facility.longitude)
            if distance <= radius_km:
                nearby_facilities.append(facility)

        serializer = self.get_serializer(nearby_facilities, many=True)
        return Response(serializer.data)