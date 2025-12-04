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
    if request.method == 'GET':
        return render(request, 'user/insert.html')
    if request.method == 'POST':
        eno = request.POST.get('emp_no', '').strip()
        first_name = request.POST.get('First_Name', '').strip()
        last_name = request.POST.get('Last_Name', '').strip()
        location = request.POST.get('Location', '').strip()
        email = request.POST.get('Email', '').strip().lower()
        salary = request.POST.get('Salary', '').strip()

        if not eno or not first_name or not last_name or not location or not email or not salary:
            messages.error(request, "All fields are required")
            return render(request, 'user/insert.html', request.POST)

        if Emp.objects.filter(empno=eno).exists():
            messages.error(request, "Employee Number already exists")
            return render(request, 'user/insert.html', request.POST)

        if Emp.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
            return render(request, 'user/insert.html', request.POST)

        if not email.endswith("@gmail.com"):
            messages.error(request, "Email must end with @gmail.com")
            return render(request, 'user/insert.html', request.POST)

        try:
            salary = int(salary)
        except:
            messages.error(request, "Salary must be a number")
            return render(request, 'user/insert.html', request.POST)

        Emp.objects.create(empno=eno,First_Name=first_name,Last_Name=last_name,Location=location,email=email,salary=salary)

        messages.success(request, "Employee added successfully")
        return redirect('selecturl')

@login_required(login_url='loginurl')
def editemp(request, eno):
    emp = Emp.objects.get(empno=eno)
    if request.method == 'GET':
        return render(request, 'user/edit.html', {'res': emp})
    if request.method == 'POST':
        emp.First_Name = request.POST.get('First_Name', '').strip()
        emp.Last_Name = request.POST.get('Last_Name', '').strip()
        emp.Location = request.POST.get('Location', '').strip()
        emp.email = request.POST.get('Email', '').strip()
        emp.salary = request.POST.get('Salary', '').strip()
        if emp.First_Name=='' or emp.Last_Name=='' or emp.Location=='' or emp.email=='' or emp.salary=='':
            messages.error('All fields are required')
            return render(request,'user/edit.html',{'res':emp})
        if Emp.objects.filter(email=emp.email).exclude(empno=eno).exists():
            messages.error(request, "Email already exists!")
            return render(request, 'user/edit.html', {'res': emp})
        if not emp.email.endswith("@gmail.com"):
            messages.error(request, "Email must end with @gmail.com")
            return render(request, 'user/edit.html', {'res': emp})
        try:
            salary = int(salary)
        except:
            messages.error(request, "Salary must be a number")
            return render(request, 'user/insert.html', request.POST)
        emp=Emp.objects.create(empno=eno, First_Name=emp.First_Name,Last_Name=emp.Last_Name,Location=emp.Location,email=emp.email,salary=emp.salary)
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
        username=request.POST.get('username', '').strip()
        password=request.POST.get('password', '').strip()
        if username=='' or password=='':
            messages.error(request,'username or password cannot be empty')
            return render(request,'user/login.html')
        valid_user=authenticate(request,username=username,password=password)
        if valid_user is None:
            messages.error(request,'Invalid username or password')
            return render(request, 'user/login.html')
        else:
            login(request,valid_user)
            return redirect('selecturl')
    return render(request, 'user/login.html')
   
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
