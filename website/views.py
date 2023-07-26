from django.shortcuts import render,redirect
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages
from .forms import SignUpForm,Recordform
from .models import Record

# Create your views here.
def home(request):
    records=Record.objects.all()
    if request.method =='POST':
        username= request.POST['username']
        password=request.POST['password']

        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            messages.success(request,"You have successfully been logged in ")
            return redirect('home')
        else:
            messages.success(request,"There was an error loggin you in please try again with the correct username and password")
            return redirect('home')
    else:    
        return render(request,'home.html',{'records':records})

#login user


def logout_user(request):
    logout(request)
    messages.success(request,"You have been successfully logged out..")
    return redirect('home')

def register_user(request):
    if request.method=='POST':
        form=SignUpForm(request.POST)
        if form.is_valid():
            form.save
            #Authenticate and login new user
            username=form.cleaned_data['username']
            password=form.cleaned_data['password1']
            user=authenticate(username=username,password=password)
            login(request,user)
            messages.success('Welcome, you have succesfully registered')
            return redirect('home')
    else:
        form=SignUpForm()
        return render(request,'register.html',{'form':form})
    return render(request,'register.html',{'form':form})


def record(request,id):
    if request.user.is_authenticated:
        #look up and return cutomer record
        record=Record.objects.get(id=id)

        return render(request,'record.html',{'record':record})
    else:
        messages.success("You have to be logged in to view this page")
        return redirect('home')


def delete_record(request,id):
    if request.user.is_authenticated:
        #look up and return the customer record
        record=Record.objects.get(id=id)
        record.delete()
        messages.success(request,"Record successfully delted")
        return redirect('home')
    else:
        messages.success(request,"You are not authorized to perform this action. Please login")
        return redirect ('home')
    

def add_record(request):
    form=Recordform(request.POST or None)

    if request.user.is_authenticated:
        if request.method=='POST':
            if form.is_valid():
                add_record=form.save()
                messages.success(request,"Record succesfuly added")
                return redirect('home')
        return render(request,'add_record.html',{'form':form})
    else:
        messages.success(request,"You are not authorized to perform this action, please login")    
        return redirect('home')


def update_record(request,id):
    if request.user.is_authenticated:
        current_record=Record.objects.get(id=id)
        form=Recordform(request.POST or None, instance=current_record)
        if form.is_valid():
            form.save
            messages.success(request,'Succesfully updated')
            return redirect('home')
        return render(request,'update_record.html',{'form':form})
    else:
        messages.success(request,"Please login to perform this action")
        return redirect('home')    
