
class StaticFilesCSPMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        if request.path.startswith('/static/'):
            response['X-Frame-Options'] = 'SAMEORIGIN'
            response['Referrer-Policy'] = 'strict-origin-when-cross-origin'
            
            if request.path.endswith('.js'):
                response['Content-Security-Policy'] = "default-src 'none'; script-src 'self' 'unsafe-inline' https://cdnjs.cloudflare.com;"
            elif request.path.endswith('.css'):
                response['Content-Security-Policy'] = "default-src 'none'; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; font-src 'self' https://fonts.gstatic.com;"
            elif request.path.endswith(('.jpg', '.png', '.webp', '.gif', '.svg')):
                response['Content-Security-Policy'] = "default-src 'self';"
            else:
                response['Content-Security-Policy'] = "default-src 'self';"
        
        return response