from django.shortcuts import render,redirect
from petapp.models import Pet
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout

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
        e = request.POST['email']
        p = request.POST['password']
        cp = request.POST['confirmpassword']
        # form validation
        if u=='' or e=='' or p=='':
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
        print(u)
        if auth == None:
            context={'error':'Please provide correct details to login'}
            return render(request,'login.html',context)
        else:
            login(request,auth)
            return redirect('/')
            
        
     
        
        
