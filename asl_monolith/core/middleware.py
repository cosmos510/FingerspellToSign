"""
Middleware de sécurité pour corriger les erreurs détectées par Screaming Frog
"""

class SecurityHeadersMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        # CORRECTION: X-Frame-Options Header manquant
        if not response.get('X-Frame-Options'):
            response['X-Frame-Options'] = 'SAMEORIGIN'
        
        # CORRECTION: Referrer-Policy Header manquant
        if not response.get('Referrer-Policy'):
            response['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        
        # CORRECTION: Content-Security-Policy Header manquant
        if not response.get('Content-Security-Policy'):
            response['Content-Security-Policy'] = (
                "default-src 'self'; "
                "script-src 'self' 'unsafe-inline' https://cdnjs.cloudflare.com https://fonts.googleapis.com; "
                "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; "
                "font-src 'self' https://fonts.gstatic.com; "
                "img-src 'self' data:; "
                "connect-src 'self';"
            )
        
        return response