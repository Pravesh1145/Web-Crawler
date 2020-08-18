from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate,logout
from django.contrib.auth.models import User
from account.forms import SignUpForm
from django.contrib.auth.decorators import login_required
from requests import get
from .models import deals
from bs4 import BeautifulSoup
import re
import json
from decimal import Decimal
def hdv():
    headers_Get = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    }
    return headers_Get
def paytmmall(query):
    urlvalu = 'https://middleware.paytmmall.com/search?channel=web&child_site_id=6&site_id=2&version=2&from=organic&items_per_page=32&userQuery='+str(query)+'&cat_tree=1'
    headers_Get = hdv()
    r = get(urlvalu, headers=headers_Get)
    data = r.json()

    ftchdata = data['grid_layout']
    y = 0
    for lt in ftchdata:
        y = y+1
        if y<=10:
            namev= lt['name']
            urlv= lt['url']
            pricev= lt['actual_price']
            mrpv = lt['offer_price']
            imagev = lt['image_url'].replace("assetscdn","assetscdn1")+str('?imwidth=282&impolicy=hq')
            entsub = deals(url=urlv, name=namev, image=imagev, mrp=mrpv, price=pricev,
                           storeimage='https://couponsdray.com/images/store/176/paytmmall-coupons-offers_1509434365.png')
            entsub.save()

def flipkart(query):
    urlvalu = 'https://www.flipkart.com/search?q='+str(query)
    headers_Get = hdv()
    r = get(urlvalu, headers=headers_Get)
    soup = BeautifulSoup(r.text, "html.parser")
    
    for tag in soup.findAll('div', {"class": "bhgxx2 col-12-12"}):
        namev = ''
        urlv = ''
        pricev = '0'
        imagev = ''
        #print tag
        name = tag.find('div', {"class": "_3wU53n"})
        if name:
            namev = name.text

            price = tag.find('div', {"class": "_1vC4OE _2rQ-NK"})
            if price:
                pricev = price.text

                
            imgdiv = tag.find('div', {"class": "hGSR34"})
            if imgdiv:
                image = imgdiv.img['src']
                imagev = image
            url = tag.find('a')
            
            urlv = url['href']
        else:
            name = tag.find('a', {"class": "_2mylT6"})
            if name:
                namev =  name.text
                #print namev
                urlv = name['href']
                price = tag.find('div', {"class": "_1vC4OE"})
                if price:
                    pricev = price.text
                imgdiv = tag.find('div', {"class": "_3ZJShS _31bMyl"})  
                if imgdiv:
                    imagev = imgdiv.img['src']

         
       
        if pricev!='0':
            pricev = pricev.replace("₹",'')
            pricev = pricev.replace(",",'')
            urlv = str('https://www.flipkart.com')+urlv
            entsub = deals(url=urlv, name=namev, image=imagev, price=pricev,storeimage='https://couponsdray.com/images/store/176/Flipkart-coupons-offers.png')
            entsub.save()            

       


def tatacliq(query):
    urlvalu = 'https://www.tataque.com/marketplacewebservices/v2/mpl/products/searchProducts/?searchText='+str(query)+'%205%3Arelevance%3AinStockFlag%3Atrue&isKeywordRedirect=false&isKeywordRedirectEnabled=true&isTextSearch=false&isFilter=false&page=0&isPwa=true&pageSize=40&typeID=all'
    headers_Get = hdv()
    r = get(urlvalu, headers=headers_Get)
    data = r.json()

    ftchdata = data['searchresult']
    y = 0
    for lt in ftchdata:
        y = y+1
        if y<=10:
            namev = lt['productname']
            urlv= str('https://www.tatacliq.com')+lt['webURL']
            pricev = lt['price']['sellingPrice']['formattedValueNoDecimal']
            mrpv = lt['price']['mrpPrice']['formattedValueNoDecimal']
            image = lt['imageURL']
            imagev = str('https:')+image
            pricev = pricev.replace("₹",'')
            mrpv = mrpv.replace("₹",'')

            entsub = deals(url=urlv, name=namev, image=imagev, mrp=mrpv, price=pricev,
                           storeimage='https://couponsdray.com/images/store/176/tatacliq-Coupons.png')
            entsub.save()
    

@login_required(login_url='/login/',redirect_field_name=None)
def home(request):
    #return HttpResponse(User)
	return render(request, 'account/index.html')
def logoutuser(request):
    #return HttpResponse(User)
    logout(request)
    return redirect('/login')    
def loginuser(request):
    error='invalid login'
    if request.method == 'POST':
        username = request.POST.get('nickname','')
        password = request.POST.get('password','')
        user = authenticate(username=username, password=password)
        if user is not None:

            if user.is_active:
                request.session.set_expiry(86400) #sets the exp. value of the session 
                login(request, user) #the user is now logged in
                return redirect('/home')
        
    else:
        return render(request, 'account/index2.html')
    
    return render(request,'account/index2.html',{"error":error})
def register1(request):
	return render(request, 'account/index3.html')
def homerequest(request):
    qr = request.GET.get('q','')
    error="Pleace Cheack Internet Connection"
    if qr:

        try:#qr = 'REEBOK'
             deals.objects.all().delete()
             tatacliq(qr) 
             paytmmall(qr)
             flipkart(qr)
    
             bannerdata = deals.objects.all().order_by('-price') 
        except: 
            return render(request,'account/index.html',{"error":error})
      
    
    return render(request, 'account/index4.html',{"bannerdata":bannerdata})    	

def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            #form.setdefault('is_staff', True)
            form.is_superuser = True
            form.is_active = True
            form.is_staff = True
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            if user is not None:

                if user.is_active:
                    login(request,user)
                    return redirect('/home')
                    return HttpResponse("login successful")
                else:
                    return HttpResponse("disabled account")
            else:
                return HttpResponse("invalid login")

            #login(request, user)
            
    else:
        form = SignUpForm()

    return render(request, 'account/index3.html', {'form': form})	

# Create your views here.
