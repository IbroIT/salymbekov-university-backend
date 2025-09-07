from django.utils import translation
from django.utils.deprecation import MiddlewareMixin

class LanguageMiddleware(MiddlewareMixin):
    """Middleware для определения языка из запроса"""
    
    def process_request(self, request):
        # Определяем язык из параметра запроса, заголовка или используем по умолчанию
        language = request.GET.get('lang') or \
                  request.META.get('HTTP_ACCEPT_LANGUAGE', '')[:2] or \
                  'ru'
        
        # Устанавливаем язык для текущего запроса
        translation.activate(language)
        request.LANGUAGE_CODE = language

class CorsMiddleware(MiddlewareMixin):
    """Middleware для обработки CORS"""
    
    def process_response(self, request, response):
        response['Access-Control-Allow-Origin'] = '*'
        response['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
        response['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        return response