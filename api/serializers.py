# from rest_framework
from rest_framework import serializers

# from 'api' app
from .models import user_details

class User_detailsSerializer(serializers.Serializer):
	id = serializers.IntegerField() 
	first_name = serializers.CharField(max_length=50)
	last_name = serializers.CharField(max_length=50)
	company_name = serializers.CharField(max_length=70)
	age = serializers.IntegerField()
	city = serializers.CharField(max_length=50)
	state = serializers.CharField(max_length=50)
	zip = serializers.IntegerField()
	email = serializers.CharField(max_length=50)
	web = serializers.CharField(max_length=50)