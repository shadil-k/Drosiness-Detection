from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from Drowsiness_Detection_App.models import User

class Userregserializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['Firstname','Lastname','Gender','Place', 'Post', 'Pin', 'Email', 'Phone', 'Vehicle']

