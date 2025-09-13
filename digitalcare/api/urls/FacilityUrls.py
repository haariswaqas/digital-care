# api/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from ..views import FacilityViewSet

router = DefaultRouter()
router.register(r'facilities', FacilityViewSet, basename='facility')

urlpatterns = [
    path('', include(router.urls)),
]
