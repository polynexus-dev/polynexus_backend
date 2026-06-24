import secrets
from functools import wraps
from django.http import JsonResponse
from .models import AdminToken

def generate_token(user):
    # Generate 64-character secure hex token
    token_str = secrets.token_hex(32)
    AdminToken.objects.create(user=user, token=token_str)
    return token_str

def staff_member_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        auth_header = request.headers.get('Authorization', '')
        if not auth_header.startswith('Bearer '):
            return JsonResponse({'error': 'Unauthorized: Bearer token required'}, status=401)
        
        token_str = auth_header.split('Bearer ')[1].strip()
        try:
            admin_token = AdminToken.objects.select_related('user').get(token=token_str)
            if not admin_token.user.is_staff:
                return JsonResponse({'error': 'Forbidden: Staff status required'}, status=403)
            
            request.user = admin_token.user
            return view_func(request, *args, **kwargs)
        except AdminToken.DoesNotExist:
            return JsonResponse({'error': 'Unauthorized: Invalid or expired token'}, status=401)
            
    return _wrapped_view
