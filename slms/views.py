
from slmsapp.EmailBackEnd import EmailBackEnd
from django.contrib.auth import login
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
import json


from django.contrib.auth import get_user_model
User = get_user_model()


@csrf_exempt
def views_Login(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('email')
            password = data.get('password')

            user = EmailBackEnd().authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                token, created = Token.objects.get_or_create(user=user)
                user_type = user.user_type
                if user_type == 1:
                    return JsonResponse({'status': 'success', 'token': token.key, 'redirect_url': 'admin/dashboard'})
                elif user_type == 2:
                    return JsonResponse({'status': 'success', 'token': token.key, 'redirect_url': 'employee/dashboard'})
                else:
                    return JsonResponse({'status': 'success', 'token': token.key, 'redirect_url': '/login'})
            else:
                return JsonResponse({'status': 'fail', 'message': 'Invalid email or password'}, status=400)

        except json.JSONDecodeError:
            return JsonResponse({'status': 'fail', 'message': 'Invalid JSON'}, status=400)

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

    return JsonResponse({'status': 'fail', 'message': 'Only POST method is allowed'}, status=405)
