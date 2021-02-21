from django.shortcuts import render ,HttpResponseRedirect
from .forms import SignUpForm , LoginForm , Postform
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout 
from .models import post
from django.contrib.auth.models import Group
# Create your views here.

def home(request):
    posts = post.objects.all()
    return render(request,'miniblog/home.html',{'posts':posts})

def about(request):
    return render(request,'miniblog/about.html')

def contact(request):
    return render(request,'miniblog/contact.html')

def dashboard(request):
    if request.user.is_authenticated:
        posts = post.objects.all()
        user = request.user
        full_name = user.get_full_name()
        gps = user.groups.all()
        return render(request,'miniblog/dashboard.html',{'posts':posts,'fullname':full_name,'groups':gps})
    else:
        return HttpResponseRedirect('/login')
    return render(request,'miniblog/dashboard.html')

def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')

def user_signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            messages.success(request,'Congratulation you have become an Author!')
            user = form.save()
            group = Group.objects.get(name='Author')
            user.groups.add(group)
    else:   
        form = SignUpForm()
    return render(request,'miniblog/signup.html',{'form':form})

def user_login(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = LoginForm(request=request, data=request.POST)
            if form.is_valid():
                uname = form.cleaned_data['username']
                pswd = form.cleaned_data['password']
                user = authenticate(username = uname, password = pswd)
                if user is not None:
                    login(request,user)
                    return HttpResponseRedirect('dashboard')
                    
        else:   
            form = LoginForm()
        return render(request,'miniblog/login.html',{'form':form})
    else:
        return HttpResponseRedirect('dashboard')
    
def delete(request,id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            posts = post.objects.get(pk=id)
            posts.delete()
        return HttpResponseRedirect('/dashboard')
    else:
        return HttpResponseRedirect('login')

def addpost(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = Postform(request.POST)
            if form.is_valid():
                title = form.cleaned_data['title']
                desc = form.cleaned_data['desc']
                pst = post(title=title,desc=desc)
                pst.save()
                form = Postform()

        else:
            form = Postform()
        return render(request,'miniblog/addpost.html',{'form':form})
    else:
        return HttpResponseRedirect('login')

def updatepost(request,id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            pi = post.objects.get(pk=id)
            form = Postform(request.POST, instance=pi)
            if form.is_valid():
                form.save()
        else:
            pi = post.objects.get(pk=id)
            form = Postform(instance=pi)
        return render(request,'miniblog/updatepost.html',{'form':form})
    else:
        return HttpResponseRedirect('login')