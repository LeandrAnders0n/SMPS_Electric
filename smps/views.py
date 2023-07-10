from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import check_password
from django.http import JsonResponse
from .models import *
import paho.mqtt.client as mqtt


def index(request):
    print("hi")
    return render(request, 'index.html')

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

def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT broker")
    # Subscribe to desired topics
    client.subscribe("topic1")
    client.subscribe("topic2")

def on_message(client, userdata, msg):
    print(f"Received message on topic: {msg.topic}")
    print(f"Message: {msg.payload.decode()}")

def mqtt_subscribe(request):
    # Define the MQTT broker and connection parameters
    broker_address = "broker.hivemq.com"
    broker_port = 1883
    username = ""  # No username required for HiveMQ public broker
    password = ""  # No password required for HiveMQ public broker

    # Create an MQTT client instance
    client = mqtt.Client()

    # Set up the callbacks
    client.on_connect = on_connect
    client.on_message = on_message

    # Connect to the MQTT broker
    client.connect(broker_address, broker_port, 60)

    # Start the MQTT loop to handle incoming messages
    client.loop_start()

    # Return a JSON response
    response_data = {'status': 'success', 'message': 'MQTT subscription started'}
    return JsonResponse(response_data)

