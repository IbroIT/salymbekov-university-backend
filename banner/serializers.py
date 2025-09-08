# banner/serializers.py
from rest_framework import serializers
from .models import Banner

class BannerSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    subtitle = serializers.SerializerMethodField()
    
    class Meta:
        model = Banner
        fields = ['image', 'title', 'subtitle']
    
    def get_title(self, obj):
        request = self.context.get('request')
        if request:
            language = request.LANGUAGE_CODE
            if language == 'ky':
                return obj.title_kg
            elif language == 'en':
                return obj.title_en
        return obj.title_ru
    
    def get_subtitle(self, obj):
        request = self.context.get('request')
        if request:
            language = request.LANGUAGE_CODE
            if language == 'ky':
                return obj.subtitle_kg
            elif language == 'en':
                return obj.subtitle_en
        return obj.subtitle_ru