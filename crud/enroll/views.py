from django.shortcuts import render,HttpResponseRedirect
from .forms import Registration
from .models import User

# Create your views here.
def add_show(request):
    if request.method == 'POST':
        fm = Registration(request.POST)
        if fm.is_valid():
            nm = fm.cleaned_data['name']
            em = fm.cleaned_data['email']
            pd = fm.cleaned_data['password']
            reg = User(name=nm,email=em,password=pd)
            reg.save()
            fm = Registration()
            
            
    else:
        fm = Registration()
    stud = User.objects.all()

    return render(request,'enroll/addandshow.html',{'form':fm , 'stu':stud})


def update_data(request,id):
    if request.method == 'POST':
        pi = User.objects.get(pk=id)
        fm = Registration(request.POST,instance=pi)
        if fm.is_valid():
            fm.save()
            return HttpResponseRedirect('/')
        
    else:
        pi = User.objects.get(pk=id)
        fm = Registration(instance=pi)
    return render(request,'enroll/updatestudent.html',{'form':fm})

def delete_data(request,id):
    if request.method == 'POST':
        pi = User.objects.get(pk=id)
        pi.delete()
        return HttpResponseRedirect('/')
