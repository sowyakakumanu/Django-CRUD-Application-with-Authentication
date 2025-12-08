from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Emp
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import UserForm
@login_required(login_url='loginurl')
def insertemp(request):
    if request.method == 'GET':
        return render(request, 'user/insert.html')
    if request.method == 'POST':
        eno = request.POST.get('emp_no', '').strip()
        first_name = request.POST.get('First_Name', '').strip()
        last_name = request.POST.get('Last_Name', '').strip()
        location = request.POST.get('Location', '').strip()
        email = request.POST.get('Email', '').lower().strip()
        salary = request.POST.get('Salary', '').strip()
        if not all([eno, first_name, last_name, location, email, salary]):
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
        except ValueError:
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
        first_name = request.POST.get('First_Name', '').strip()
        last_name = request.POST.get('Last_Name', '').strip()
        location = request.POST.get('Location', '').strip()
        email = request.POST.get('Email', '').lower().strip()
        salary = request.POST.get('Salary', '').strip()
        if not all([first_name, last_name, location, email, salary]):
            messages.error(request, "All fields are required")
            return render(request, 'user/edit.html', {'res': emp})
        if Emp.objects.filter(email=email).exclude(empno=eno).exists():
            messages.error(request, "Email already exists!")
            return render(request, 'user/edit.html', {'res': emp})
        if not email.endswith("@gmail.com"):
            messages.error(request, "Email must end with @gmail.com")
            return render(request, 'user/edit.html', {'res': emp})
        try:
            salary = int(salary)
        except ValueError:
            messages.error(request, "Salary must be a number")
            return render(request, 'user/edit.html', {'res': emp})
        emp.First_Name = first_name
        emp.Last_Name = last_name
        emp.Location = location
        emp.email = email
        emp.salary = salary
        emp.save()
        messages.success(request, "Updated successfully")
        return redirect('selecturl')
@login_required(login_url='loginurl')
def selectemp(request):
    emps = Emp.objects.all()
    return render(request, 'user/select.html', {'res': emps})
@login_required(login_url='loginurl')
def deleteemp(request, eno):
    emp = Emp.objects.get(empno=eno)
    if request.method == 'GET':
        return render(request, 'user/delete.html', {'res': emp})
    if request.method == 'POST':
        emp.delete()
        return redirect('selecturl')
def loginpage(request):
    if request.method == 'GET':
        return render(request, 'user/login.html')
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        if not username or not password:
            messages.error(request, "Username or password cannot be empty")
            return render(request, 'user/login.html')
        user = authenticate(request, username=username, password=password)
        if user is None:
            messages.error(request, "Invalid username or password")
            return render(request, 'user/login.html')
        login(request, user)
        return redirect('selecturl')
def logoutpage(request):
    logout(request)
    return redirect('loginurl')
def registerpage(request):
    if request.method == 'GET':
        form = UserForm()
        return render(request, 'user/register.html', {'form': form})
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registered successfully")
            return redirect('loginurl')
        else:
            return render(request, 'user/register.html', {'form': form})
