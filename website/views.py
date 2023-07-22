from django.shortcuts import render,redirect
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages
# Create your views here.
def home(request):

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
        return render(request,'home.html',{})

#login user


def logout_user(request):
    logout(request)

