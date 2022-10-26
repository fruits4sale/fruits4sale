from django.shortcuts import render
from .models import *
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import *
from django.contrib import messages

# Create your views here.

def home(request):
	searchTerm = request.GET.get('searchMovie')
	if searchTerm:
		fruitdata = Fruits.objects.filter(fruit_name__icontains=searchTerm)
		context = {'searchTerm':searchTerm, 'fruitdata': fruitdata}
	else:
		fruitdata = Fruits.objects.all()
		context = {'searchTerm':searchTerm, 'fruitdata': fruitdata}
	return render(request, 'home.html',context	)


@login_required
def purchase(request, fruit_id):
	fruitdata = Fruits.objects.get(pk=fruit_id)
	form = PurchaseForm(request.POST)
	if request.method == "POST":
		newPurchase = form.save(commit=False)
		newPurchase.user = request.user
		newPurchase.fruit = fruitdata
		newPurchase.total_amount = float(float(fruitdata.price_per_quantity) * int(newPurchase.quantity_purchased))
		if int(fruitdata.quantity) < int(newPurchase.quantity_purchased):
			messages.error(request, 'Quantity Purchased Exceeded the Quantity remaining of the Product. Please Try Again')
			return redirect('purchase', fruit_id)
		else:
			newPurchase.save()
			updateFruitQuantity(fruit_id, newPurchase.quantity_purchased)
			messages.success(request, 'Purchased Successfully. You can now view your Purchases in MyCart ')
			return redirect('purchase', fruit_id)
	context = {'fruitdata': fruitdata, 'form':form}
	return render(request, 'purchase.html', context)

def updateFruitQuantity(fruit_id, purchased_quantity):
	fruitdata = Fruits.objects.get(pk=fruit_id)
	fruitdata.quantity = int(fruitdata.quantity) - int(purchased_quantity)
	fruitdata.save()

@login_required
def myCart(request):

	cartData = MyCart.objects.filter(user = request.user)
	context = {'cartData':cartData}
	return render(request, 'myCart.html', context)



