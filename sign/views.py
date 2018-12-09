from django.shortcuts import render

from django.http import HttpResponse,HttpResponseRedirect
from django.contrib import auth

# Create your views here.
#import requests
from django.shortcuts import render
from sign.models import Event,Guest,User
from sign.dao.userDao import *

def index(request):
    #return HttpResponse("hel1qwlo Django")
    return render(request,'index.html')

#登录方法
def login_action(request):
    if request.method =='POST':
        username = request.POST.get('username','')
        password = request.POST.get('password','')

        if username == '' or password =='':
            return render(request, 'index.html', {'input_error': '用户名或者密码不能为空'})


        user_list= get_user(username,password)
        print('user_lsit======',user_list)
       #user = auth.authenticate(username = username,password=password)
        user_lists = []
        for userl in user_list:
            user_lists.append(userl)

        print("user_lists = ==",user_lists)
        print('user_lists长度===',len(user_lists))
        if  len(user_lists) ==0:
            print("if  user_list =='':")
            return render(request, 'index.html', {'input_error': '用户名或者密码错误'})
        request.session['user'] = user_list[0].account
        if user_list[0].role == 0:
            response = HttpResponseRedirect('/administrator/')
            return response
        else:
            response = HttpResponseRedirect('/event_manage/')
            return response
        #if username =='admin' and password =='admin123':
        # if user is not None:
        #     auth.login(request,user)
            #return HttpResponse('登录成功')
            #response = HttpResponseRedirect('/event_manage/')
            #response.set_cookie('user',username,3600)
            #request.session['user'] = username
            #return response
            #return HttpResponseRedirect('/event_manage/')

       # return render(request,'index.html',{'input_error':'用户名或者密码错误'})
#定义登陆成功后发布会管理页面
def event_manage(request):
    #username = request.COOKIES.get('user','')
    username = request.session.get('user','')

    event_list = Event.objects.all()
    #print('event_list',event_list)

    return render(request,'event_manage.html',{'user':username,"events":event_list})
def administrator(request):
    return render(request,'administrator.html')