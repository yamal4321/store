from django.shortcuts import render
from .models import Seller
from .models import Product 
from django.views.decorators.csrf import csrf_exempt
import re
from django import forms
from PIL import Image
from io import BytesIO 
from django.db import connection
import json
from .rnn import predict 

def cart_sum():
  cursor = connection.cursor()
  cursor.execute('''SELECT sum(price) FROM front_product, cart WHERE front_product.uuid = cart.uuid''')
  s = list(cursor)[0][0]
  return 0 if s is None else s

@csrf_exempt
def home(request):
  data = []
  for product in Product.objects.all():
    name = Seller.objects.filter(uuid=product.user_uuid_id).first().name
    data.append({**product.__dict__, **{'user_name': name}})

  if request.method == 'POST': 
    data = json.loads(request.body.decode())
    if "uuid" in data: 
      cursor = connection.cursor()
      cursor.execute("""UPDATE front_product SET votes = votes + 1 WHERE uuid="%s";""" % (str(data["uuid"]).replace('-', '')));
    if "history" in data: 
      cursor = connection.cursor()
      cursor.execute("""INSERT INTO history (visited) VALUES("%s");""" % (str(data["history"])));
    if "remove_uuid" in data: 
      cursor = connection.cursor()
      cursor.execute("""DELETE FROM front_product WHERE uuid="%s";""" % (str(data["remove_uuid"]).replace('-', '')));

  return render(request, 'front/front_page.html', {'context': data, 'cart': cart_sum()})

@csrf_exempt
def recommended(request):
  objects = predict()
  if len(objects)==0: return home(request)
  data = []
  for product in objects:
    name = Seller.objects.filter(uuid=product.user_uuid_id).first().name
    data.append({**product.__dict__, **{'user_name': name}})

  return render(request, 'front/recommended.html', {'context': data, 'cart': cart_sum()})

class SellForm(forms.Form):
  seller = forms.CharField(label="seller", max_length=100)
  email = forms.CharField(label="email", max_length=100, required=False) 
  name = forms.CharField(label="name", max_length=100, required=False) 
  description = forms.CharField(label="description", required=False) 
  price = forms.IntegerField(label="price")
  details = forms.CharField(label="details", max_length=1000, required=False) 
  delivery = forms.CharField(label="delivery", max_length=1000, required=False) 
  contacts = forms.CharField(label="contacts", max_length=1000, required=False) 
  photo = forms.ImageField(label="photo")

@csrf_exempt
def sell(request):
  if request.method == "POST" and SellForm(request.POST, request.FILES).is_valid(): 
    form = SellForm(request.POST, request.FILES)
    name = request.FILES["photo"].name
    im = Image.open(BytesIO(request.FILES['photo'].read()))
    im.save("front/static/front/%s" % (name), "PNG")

    seller1 = Seller(name=request.POST['seller'], email=request.POST['email'])
    seller1.save()
    product1 = Product(name=request.POST['name'], description=request.POST['description'], price=request.POST['price'], details=request.POST['details'], \
      delivery=request.POST['delivery'], contacts=request.POST['contacts'], photo=name, category=request.POST['category'], user_uuid_id=seller1.uuid)
    product1.save()
      
  return render(request, 'front/seller_form.html', {'cart': cart_sum()})

@csrf_exempt
def product(request):
  _uuid = re.search('products/(.+)', request.build_absolute_uri()).group(1)
  product = Product.objects.filter(uuid=_uuid).first()
  if request.method == 'POST' and request.POST.get("cart"):
    cursor = connection.cursor()
    cursor.execute("""INSERT INTO cart VALUES("%s");""" % (str(_uuid).replace('-', '')));
  return render(request, 'front/product_info.html', {'context': product.__dict__, 'cart': cart_sum()})

@csrf_exempt
def cart(request):
  if request.method == 'POST':
    data = json.loads(request.body.decode())
    if "uuid" in data:
      cursor = connection.cursor()
      cursor.execute("""DELETE FROM cart WHERE uuid="%s" LIMIT 1;""" % (str(data["uuid"]).replace('-', '')));

  cursor = connection.cursor()
  cursor.execute('''SELECT front_product.* FROM front_product, cart WHERE front_product.uuid = cart.uuid''')
  columns = [*zip(*cursor.description)][0]
  data = [dict(zip(columns, x)) for x in cursor.fetchall()] 

  return render(request, 'front/front_cart.html', {'context': data, 'cart': cart_sum()})
