from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Fruits(models.Model):
	fruit_name = models.CharField(max_length=100)
	description = models.CharField(max_length=100)
	image = models.ImageField(upload_to='movie/images/')
	quantity = models.IntegerField()
	units = models.CharField(max_length=100)
	price_per_quantity = models.FloatField()

	def __str__(self):
		return self.fruit_name



class MyCart(models.Model):    
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    fruit = models.ForeignKey(Fruits,on_delete=models.CASCADE)
    quantity_purchased = models.IntegerField()
    total_amount = models.FloatField()
    date = models.DateTimeField(auto_now_add=True)  

    def __str__(self):
        return f'{self.user.username} | {self.fruit.fruit_name}'


