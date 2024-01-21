# from rest_framework
from rest_framework import serializers

# from 'api' app
from models import *

class User_detailsSerializer(serializers.Serializer):
	id = serializers.IntegerField(primary_key=True) 
	first_name = serializers.CharField(max_length=50)
	last_name = serializers.CharField(max_length=50)
	company_name = serializers.CharField(max_length=70,null=True)
	age = serializers.IntegerField()
	city = serializers.CharField(max_length=50)
	state = serializers.CharField(max_length=50)
	zip = serializers.IntegerField()
	email = serializers.CharField(max_length=50,unique=True)
	web = serializers.CharField(max_length=50)