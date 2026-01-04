from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def test_headers(request):
    """Vue de test pour vérifier les headers de sécurité"""
    response = HttpResponse("Headers test")
    response['X-Frame-Options'] = 'SAMEORIGIN'
    response['Referrer-Policy'] = 'strict-origin-when-cross-origin'
    response['Content-Security-Policy'] = "default-src 'self'; script-src 'self' 'unsafe-inline' https://cdnjs.cloudflare.com; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; font-src 'self' https://fonts.gstatic.com; img-src 'self' data:; connect-src 'self';"
    return response