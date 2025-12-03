from django.shortcuts import render,redirect
from django.http import HttpResponse
from . models import Emp
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from .forms import UserForm
# Create your views here.
@login_required(login_url='loginurl')
def insertemp(request):
    if request.method=='GET':
        emps=Emp.objects.all()
        return render(request,'user/insert.html')
    if request.method=='POST':
        eno=int(request.POST['emp_no'])
        first_name=request.POST['First_Name']
        last_name=request.POST['Last_Name']
        location=request.POST['Location']
        email=request.POST['Email']
        salary=int(request.POST['Salary'])
        eobj=Emp.objects.create(empno=eno,First_Name=first_name,Last_Name=last_name,Location=location,email=email,salary=salary)
        eobj.save()
        return redirect('selecturl')

@login_required(login_url='loginurl')
def editemp(request, eno):
    emp = Emp.objects.get(empno=eno)
    if request.method == 'GET':
        return render(request, 'user/edit.html', {'res': emp})
    if request.method == 'POST':
        emp.First_Name = request.POST['First_Name']
        emp.Last_Name = request.POST['Last_Name']
        emp.Location = request.POST['Location']
        emp.email = request.POST['Email']
        emp.salary = int(request.POST['Salary'])
        emp.save()
        messages.success(request,'updated sucessfully')
        return redirect('selecturl')
        
@login_required(login_url='loginurl')
def selectemp(request):
    if request.method=='GET':
        emps=Emp.objects.all()
        return render(request,'user/select.html',{'res':emps})

@login_required(login_url='loginurl')
def deleteemp(request,eno):
    emps=Emp.objects.get(empno=eno)
    if request.method=='GET':
        return render(request,'user/delete.html',{'res':emps})
    if request.method=='POST':
        emps.delete()
        return redirect('selecturl')
    
def loginpage(request):
    if request.method=='GET':
        return render(request,'user/login.html')
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        valid_user=authenticate(request,username=username,password=password)
        if valid_user is None:
            return redirect('loginurl')
        else:
            login(request,valid_user)
            return redirect('selecturl')
        
def logoutpage(request):
    logout(request)
    return redirect('loginurl')

def registerpage(request):
    if request.method=='GET':
        Emptyform=UserForm()
        return render(request,'user/register.html',{'form':Emptyform})
    if request.method=='POST':
        Dataform=UserForm(request.POST)
        if Dataform.is_valid()==True:
            Dataform.save()
            messages.success(request,'registered sucessfully')
            return redirect('loginurl')
        else:
            return render(request,'user/register.html',{'form':Dataform})
