from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.hashers import make_password



#make migrations
class Role(models.Model):
    name = models.CharField(max_length=100)
    role_id = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(3)]
    )

class User(models.Model):
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=128)
    role_id = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(3)]
    )

class Tower(models.Model):
    area_manager_id = models.ForeignKey(User, on_delete=models.CASCADE)
    lat = models.DecimalField(max_digits=9, decimal_places=6)
    long = models.DecimalField(max_digits=9, decimal_places=6)
    assigned = models.IntegerField(default=0, choices=((0, 'Not Assigned'), (1, 'Assigned')))

class Operator(models.Model):
    tower_id = models.ForeignKey(Tower, on_delete=models.CASCADE)
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE)
    assigned_by = models.ForeignKey(User, on_delete=models.CASCADE)
    lat = models.DecimalField(max_digits=9, decimal_places=6)
    long = models.DecimalField(max_digits=9, decimal_places=6)

class Device(models.Model):
    info = models.TextField()
    tower_id = models.ForeignKey(Tower, on_delete=models.CASCADE)

class SensorMaster(models.Model):
    device_id = models.ForeignKey(Device, on_delete=models.CASCADE)
    name=models.CharField(max_length=128)
    min = models.IntegerField()
    max = models.IntegerField()

class SensorValues(models.Model):
    sensor_id = models.ForeignKey(SensorMaster, on_delete=models.CASCADE)
    value=models.CharField(max_length=128)
    timestamp = models.DateTimeField(auto_now_add=True)
    


#seed db
def initRole():
        user_type1 = Role.objects.create(name='Director',role_id=0 )
        user_type2 = Role.objects.create(name='Area Manager',role_id=1)
        user_type3 = Role.objects.create(name='Operator', role_id=2)
        user_type4 = Role.objects.create(name='User', role_id=3)
        user_type1.save()
        user_type2.save()
        user_type3.save()
        user_type4.save()

def initUser():
        user1 = User.objects.create(email='director@gmail.com',password=make_password('123'),role_id=0 )
        user2 = User.objects.create(email='area_manager@gmail.com',password=make_password('123'),role_id=1)
        user1.save()
        user2.save()

# initRole()
# initUser()