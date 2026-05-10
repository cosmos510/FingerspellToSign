import os
from django.http import HttpResponseForbidden


class IPBlockMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        blocked = os.getenv('BLOCKED_IPS', '')
        self.blocked_ips = set(ip.strip() for ip in blocked.split(',') if ip.strip())

    def __call__(self, request):
        ip = self.get_client_ip(request)
        if ip in self.blocked_ips:
            return HttpResponseForbidden('Access denied')
        return self.get_response(request)

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0].strip()
        return request.META.get('REMOTE_ADDR')


class SecurityHeadersMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        response['X-Frame-Options'] = 'SAMEORIGIN'
        response['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        
        if request.path.endswith(('.js', '.css')):
            response['Content-Security-Policy'] = (
                "default-src 'none'; "
                "script-src 'self' 'unsafe-inline' https://cdnjs.cloudflare.com; "
                "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; "
                "font-src 'self' https://fonts.gstatic.com;"
            )
        else:
            response['Content-Security-Policy'] = (
                "default-src 'self'; "
                "script-src 'self' 'unsafe-inline' https://cdnjs.cloudflare.com https://fonts.googleapis.com; "
                "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; "
                "font-src 'self' https://fonts.gstatic.com; "
                "img-src 'self' data:; "
                "connect-src 'self';"
            )
        
        return response