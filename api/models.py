from django.db import models

# Table to store user details
class user_details(models.Model):
    id = models.IntegerField(primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    company_name = models.CharField(max_length=70,null=True)
    age = models.IntegerField()
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    zip = models.IntegerField()
    email = models.CharField(max_length=50)
    web = models.CharField(max_length=50)

    class Meta:
        unique_together = ('id', 'first_name',)