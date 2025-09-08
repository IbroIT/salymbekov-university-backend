# banner/views.py
from rest_framework import generics
from .models import Banner
from .serializers import BannerSerializer

class BannerListAPIView(generics.ListAPIView):
    serializer_class = BannerSerializer
    queryset = Banner.objects.filter(is_active=True)
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context