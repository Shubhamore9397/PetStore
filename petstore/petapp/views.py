from django.shortcuts import render,redirect
from petapp.models import Pet,Cart,Order
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.db.models import Q #used at searchByRange function for applying filteration of price ranges
import razorpay
import random
from django.core.mail import send_mail

# Create your views here.
def home(request):
    # return render(request, 'index.html')
    # return render(request, 'base.html')
    # return render(request, 'index2.html')
    context={}
    data = Pet.objects.all()
    context['pets']=data
    return render(request,'index.html',context)

def showPetDetails(request,rid):
    context={}
    data= Pet.objects.get(id=rid)
    context['pet']=data
    return render(request,'details.html',context)

def registerUser(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    else:
        u = request.POST['username']
        # if User.objects.get(username=u) is not None:
        #     context={'error':'Username already registered. Please enter a different username for registration'}
        #     return render(request,'register.html',context)  commented due error while registration
       
        e = request.POST['email']
        p = request.POST['password']
        cp = request.POST['confirmpassword']
        # form validation
        if u=='' or e=='' or p==''
            context={'error':'All fields are compulsory'}
            return render(request, 'register.html',context)
        elif p!=cp:
            context={'error':'Password and confirm password must be same'}
            return render(request, 'register.html',context)
        else:
            u = User.objects.create(username=u, email=e)
            u.set_password(p) # for password encription
            u.save()
            messages.success(request,'Registered successfully, Please login')
            return redirect('/login')
        
def userLogin(request): 
    if request.method == 'GET':
        return render(request,'login.html')
    else:
        # login activity
        u= request.POST['username']
        p= request.POST['password']
        auth= authenticate(username=u, password=p)
        print('logged in user',auth)
        if auth == None:
            context={'error':'Please provide correct details to login'}
            return render(request,'login.html',context)
        else:
            login(request,auth)
            return redirect('/')
        
def userLogout(request):
    logout(request)
    messages.success(request,'User logged out successfully')
    return redirect('/')

def addtocart(request,petid):
    userid = request.user.id
    context={}
    if userid is None:
        context['error']='Please login so as to add the Pet in your cart'
        return render(request,'login.html',context)
    else:
        # cart will be added if pet and user object is known
        user = User.objects.filter(id=userid)
        pet = Pet.objects.filter(id=petid)
        cart = Cart.objects.create(uid=user, pid=pet)

        cart.save()
        messages.success(request,'Pet added to cart successfully')
        return redirect('/')
    
def showUserCart(request):
    user=request.user
    cart= Cart.objects.filter(uid=user.id)
    totalBill=0
    for c in cart:
        totalBill += c.pid.price * c.quantity
    count= len(cart)
    context={}
    context['cart']=cart
    context['total']=totalBill
    context['count']=count
    return render(request,'showcart.html',context) 

def removeCart(request,cartid):
    cart= Cart.objects.filter(id=cartid)
    cart.delete()
    messages.success(request,'Pet removed from your cart')
    return redirect('/showcart')

def updateCart(request,opr,cartid):
    cart=Cart.objects.filter(id=cartid) #returns mutiple number of query sets
    if opr == '1':
        cart.update(quantity = cart[0].quantity+1)
    else:
        cart.update(quantity = cart[0].quantity-1)
        return redirect('/showcart')
    
def searchByType(request,pet_type):
    petlist =  Pet.objects.filter(type = pet_type)
    context={'pets':petlist}
    return render(request,'index.html',context)

def searchByRange(request):
    #range?min=24000&max=28000/
    min= request.GET['min']
    max= request.GET['min']
    c1= Q(price__get = min)            
    c2= Q(price__get = max)        
    petList= Pet.objects.filter(c1 & c2)
    context= {'pets': petList}
    return render(request,'index.html',context)    

def sortByPrice(request,dir):
    col=''
    if dir == 'asc':
        col='price'
    else: #dir='desc':
        col='-price'
    petList= Pet.objects.all().order_by(col)
    context= {'pets': petList}
    return render(request,'index.html',context) 
    
def confirmOrder(request):
    user=request.user
    cart= Cart.objects.filter(uid=user.id)
    totalBill=0
    for c in cart:
        totalBill += c.pid.price * c.quantity
    count= len(cart)
    context={}
    context['cart']=cart
    context['total']=totalBill
    context['count']=count
    return render(request,'confirmorder.html',context) 

def makepayment(request):
    user = request.user
    usercart = Cart.objects.filter(uid = user.id)
    totalBill=0
    for c in cart:
        totalBill += c.pid.price * c.quantity
     
    client = razorpay.Client(auth=("rzp_test_CUovvl8j2gLttO", "xwCCTZ6uXUt8MctphYXlwVcP"))
    data = { "amount": 500, "currency": "INR", "receipt": "" }
    payment = client.order.create(data=data)
    context = {'data': payment}
    return render(request,'pay.html',context)
        
def placeOrder(request):
    # 1. place order (insert order details in order table)
    user= request.user
    mycart= Cart.objects.filter(uid=user.id)
    oId= random.randrange(10000,99999)
    # verify if its not existing in db
    for cart in mycart:
        order= Order.objects.create(orderId=oId, uid=cart.id, pid=cart.pid, quantity=cart.quantity)
        order.save()
    # 2. clear Cart
    mycart.delete()
    
    # 3. sending gmail
    msg_body= 'oder id is:'+str(oId)
    custEmail= request.user.email
    send_mail(
    "Order placed successfully", #subject
    msg_body,
    "shubhamore9397@gmail.com", #from 
    [custEmail],
    fail_silently= False    
    )
    messages.success(request,'Order placed successfully')
    return redirect('/')
    
   


    
   
  
        
        
