from django.db import models

# Create your models here.

class user_type(models.Model):
	caption = models.CharField(max_length=32, unique=True)

class usergroup(models.Model):
	name = models.CharField(max_length=32)

class user_info(models.Model):
	username = models.CharField(max_length=32)
	email = models.EmailField()
	usertype = models.ForeignKey(to='user_type', to_field='caption', on_delete=models.CASCADE)
	u2g = models.ManyToManyField(usergroup)




