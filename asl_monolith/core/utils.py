"""
Utilitaires pour ajouter les headers de sécurité aux fichiers statiques
"""

def add_security_headers(headers, path, url):
    """
    Ajoute les headers de sécurité aux fichiers statiques servis par WhiteNoise
    """
    # Headers de sécurité pour tous les fichiers statiques
    headers['X-Frame-Options'] = 'SAMEORIGIN'
    headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
    
    # CSP spécifique selon le type de fichier
    if path.endswith('.js'):
        headers['Content-Security-Policy'] = (
            "default-src 'none'; "
            "script-src 'self' 'unsafe-inline' https://cdnjs.cloudflare.com; "
        )
    elif path.endswith('.css'):
        headers['Content-Security-Policy'] = (
            "default-src 'none'; "
            "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; "
            "font-src 'self' https://fonts.gstatic.com; "
        )
    else:
        headers['Content-Security-Policy'] = "default-src 'self';"
    
    return headers