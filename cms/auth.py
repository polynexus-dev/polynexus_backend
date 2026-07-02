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
        token_str = None
        auth_header = request.headers.get('Authorization', '')
        if auth_header.startswith('Bearer '):
            token_str = auth_header.split('Bearer ')[1].strip()
        else:
            token_str = request.COOKIES.get('admin_token')

        if not token_str:
            return JsonResponse({'error': 'Unauthorized: Authentication required'}, status=401)
        
        try:
            admin_token = AdminToken.objects.select_related('user').get(token=token_str)
            
            # Check expiration (24 hours)
            from django.utils import timezone
            import datetime
            if timezone.now() - admin_token.created_at > datetime.timedelta(hours=24):
                admin_token.delete()
                return JsonResponse({'error': 'Unauthorized: Session expired'}, status=401)
            
            if not admin_token.user.is_staff:
                return JsonResponse({'error': 'Forbidden: Staff status required'}, status=403)
            
            request.user = admin_token.user
            return view_func(request, *args, **kwargs)
        except AdminToken.DoesNotExist:
            return JsonResponse({'error': 'Unauthorized: Invalid or expired token'}, status=401)
            
    return _wrapped_view
