from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import check_password
from django.http import JsonResponse
from .models import *


@csrf_exempt
def auth(request):
    try:
        if request.method == 'POST':
            email = request.POST.get('email')
            password = request.POST.get('password')
            user = User.objects.get(email=email)
            if check_password(password, user.password):
                response_data = {'message': 'Authenticated'}
                request.session['user_id'] = user.id
                return JsonResponse(response_data)
            else:
                response_data = {'message': 'Incorrect Password'}
                return JsonResponse(response_data)
        else:
            response_data = {'message': 'Method Not Allowed'}
    except User.DoesNotExist:
        response_data = {'message': 'User Does not Exist'}     
        return JsonResponse(response_data)

@csrf_exempt
def add_user(request):
    user_id = request.session.get('user_id')
    user_type = request.POST.get('user_type')    

    if int(user_type) == 1:
        print("Checking permission...")
        if check_permission(user_id, [0]):
            insert_user(request.POST.get('email'),request.POST.get('password'),user_type)
            response_data = {'message': 'User Added'}     
            return JsonResponse(response_data)
    elif int(user_type) == 2:
        print("Checking permission...")
        if check_permission(user_id, [0,1]):
            response_data = {'message': 'User Added'}    
            insert_user(request.POST.get('email'),request.POST.get('password'),user_type) 
            return JsonResponse(response_data)
    
    response_data = {'message': 'You are not Authorized for this Action'}
    return JsonResponse(response_data)

def insert_user(email,password,role):
    user = User()
    user.email=email
    user.password=make_password(password)
    user.role_id=role
    user.save()

def check_permission(id,required_role_id):
    user = User.objects.get(id=id)
    if user.role_id in required_role_id:
        return True
    else:
        return False


def index(request):
    print("hi")
    return render(request, 'index.html')

