from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError
from .models import User
import json
from django.contrib.auth.hashers import make_password, check_password

@csrf_exempt
def index(request):
    if request.method == 'POST':
        return JsonResponse({'message':'Data received'})
    else :
        return HttpResponse('jai bhole')

@csrf_exempt
def signup(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            if not all(key in data for key in ['name', 'email', 'password']):
                return JsonResponse({'error': 'Missing required fields'}, status=400)
            
            # Validate password length
            if len(data['password']) < 8:
                return JsonResponse({'error': 'Password must be at least 8 characters long'}, status=400)
            
            # Validate name length
            if len(data['name'].strip()) < 2:
                return JsonResponse({'error': 'Name must be at least 2 characters long'}, status=400)
            
            # Check if user already exists
            try:
                if User.objects.filter(email=data['email']).exists():
                    return JsonResponse({'error': 'Email already registered'}, status=400)
                
                # Create new user
                user = User(
                    name=data['name'].strip(),
                    email=data['email'].lower(),
                    password=make_password(data['password'])
                )
                user.save()
                
                return JsonResponse({
                    'message': 'User created successfully',
                    'user': {
                        '_id': str(user._id),
                        'name': user.name,
                        'email': user.email
                    }
                }, status=201)
                
            except ValidationError as e:
                return JsonResponse({'error': str(e)}, status=400)
            
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def signin(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            if not all(key in data for key in ['email', 'password']):
                return JsonResponse({'error': 'Missing required fields'}, status=400)
            
            # Check if user exists
            try:
                user = User.objects.get(email=data['email'])
            except User.DoesNotExist:
                return JsonResponse({'error': 'User not found, please signup first'}, status=404)
            
            # Check password using the stored hashed password
            if check_password(data['password'], user.password):
                return JsonResponse({
                    'message': 'Signin successful',
                    'user': {
                        '_id': str(user._id),
                        'name': user.name,
                        'email': user.email
                    }
                })
            else:
                return JsonResponse({'error': 'Invalid password'}, status=401)
            
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)

