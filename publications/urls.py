from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'publications', views.PublicationViewSet)
router.register(r'research-centers', views.ResearchCenterViewSet)

urlpatterns = [
    path('', include(router.urls)),
]