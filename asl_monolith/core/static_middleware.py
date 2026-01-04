"""
Middleware pour ajouter les headers CSP aux fichiers statiques
"""

class StaticFilesCSPMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        # Vérifier si c'est un fichier statique
        if request.path.startswith('/static/'):
            # Headers de sécurité pour tous les fichiers statiques
            response['X-Frame-Options'] = 'SAMEORIGIN'
            response['Referrer-Policy'] = 'strict-origin-when-cross-origin'
            
            # CSP spécifique selon le type de fichier
            if request.path.endswith('.js'):
                response['Content-Security-Policy'] = "default-src 'none'; script-src 'self' 'unsafe-inline' https://cdnjs.cloudflare.com;"
            elif request.path.endswith('.css'):
                response['Content-Security-Policy'] = "default-src 'none'; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; font-src 'self' https://fonts.gstatic.com;"
            elif request.path.endswith(('.jpg', '.png', '.webp', '.gif', '.svg')):
                response['Content-Security-Policy'] = "default-src 'self';"
            else:
                response['Content-Security-Policy'] = "default-src 'self';"
        
        return response