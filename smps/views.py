from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import check_password
from django.http import JsonResponse
from .models import *
import paho.mqtt.client as mqtt
import time
import json

def index(request):
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
            insert_user(request.POST.get('email'), request.POST.get('password'), user_type)
            response_data = {'message': 'User Added'}
            return JsonResponse(response_data)
    elif int(user_type) == 2:
        print("Checking permission...")
        if check_permission(user_id, [0, 1]):
            response_data = {'message': 'User Added'}
            insert_user(request.POST.get('email'), request.POST.get('password'), user_type)
            return JsonResponse(response_data)

    response_data = {'message': 'You are not Authorized for this Action'}
    return JsonResponse(response_data)


def insert_user(email, password, role):
    user = User()
    user.email = email
    user.password = make_password(password)
    user.role_id = role
    user.save()

@csrf_exempt
def add_tower(request):
    user_id = request.session.get('user_id')
    area_manager_id = request.POST.get('area_manager_id')
    latitude = request.POST.get('latitude')
    longitude = request.POST.get('longitude')

    if check_permission(user_id, [0]):
        insert_tower(area_manager_id, latitude, longitude)
        response_data = {'message': 'Tower Added'}
        return JsonResponse(response_data)
    response_data = {'message': 'You are not Authorized for this Action'}
    return JsonResponse(response_data)

def insert_tower(area_manager_id, latitude, longitude):
    user = User.objects.get(id=area_manager_id) 
    tower = Tower()
    tower.area_manager_id = user
    tower.lat = latitude
    tower.long = longitude
    tower.save()

@csrf_exempt
def assign_tower(request):
    operator_id = request.POST.get('operator_id')
    tower_id = request.POST.get('tower_id')

    user_id = request.session.get('user_id')
    if check_permission(user_id, [0, 1]):
        user = User.objects.get(id=operator_id) 
        tower = Tower.objects.get(id=tower_id) 
        operation = Operator()
        operation.tower_id = tower
        operation.assigned_to = user
        operation.save()

        tower.assigned=1
        tower.save()
        response_data = {'message': 'Tower Assigned'}
        
        return JsonResponse(response_data)

    response_data = {'message': 'You are not Authorized for this Action'}
    return JsonResponse(response_data)

def check_permission(id, required_role_id):
    user = User.objects.get(id=id)
    if user.role_id in required_role_id:
        return True
    else:
        return False

def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT broker with result code: " + str(rc))
    # Subscribe to desired topics here if needed
    client.subscribe("your/topic")  # Subscribe to the topic where data is published

def on_message(client, userdata, msg):
    if msg.topic == "your/topic":  # Replace with the subscribed topic
        # Decode the message payload
        data = json.loads(msg.payload.decode("utf-8"))

        # Print the received data
        print("Received data:", data["name"])

def publish_data(client):
    topic = "your/topic"  # Specify the topic to which you want to publish the data

    # Create dummy JSON data
    dummy_data = {
        "name": "John Doe",
        "age": 30,
        "city": "New York"
    }

    # Convert the dummy JSON data to a string
    payload = json.dumps(dummy_data)

    # Publish the JSON data to the specified topic
    client.publish(topic, payload)

def mqtt_subscribe(request):
    broker_address = "broker.hivemq.com"
    broker_port = 1883
    username = ""  # No username required for HiveMQ public broker
    password = ""  # No password required for HiveMQ public broker

    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    try:
        client.connect(broker_address, broker_port, 60)
        client.loop_start()

        time.sleep(30)

        publish_data(client)

        time.sleep(10)  # Wait for messages to be received and printed

        client.loop_stop()
        client.disconnect()

        response_data = {'status': 'success', 'message': 'MQTT subscription completed'}
    except TimeoutError:
        response_data = {'status': 'error', 'message': 'Timeout occurred while connecting to MQTT broker'}
    except Exception as e:
        response_data = {'status': 'error', 'message': f'Error occurred: {str(e)}'}

    return JsonResponse(response_data)


