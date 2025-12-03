from django.urls import path
from . import views

urlpatterns=[
    path('insert/',views.insertemp,name='inserturl'),
    path('edit/<int:eno>/',views.editemp,name='editurl'),
    path('select/',views.selectemp,name='selecturl'),
    path('delete/<int:eno>/',views.deleteemp,name='deleteurl'),
    path('login/',views.loginpage,name='loginurl'),
    path('logout/',views.logoutpage,name='logouturl'),
    path('register/',views.registerpage,name='registerurl'),
]