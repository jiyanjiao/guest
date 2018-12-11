from django.shortcuts import render

from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render,get_object_or_404
from django.contrib import auth

# Create your views here.
#import requests
from django.shortcuts import render
from sign.models import Event,Guest,User
from sign.dao.userDao import *

from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger

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


#定义admin登录后显示的后台页面,主要负责对数据库数据的增删改查


def administrator(request):
    return render(request,'administrator.html')

#定义嘉宾


def guest_manage(request):
    username = request.session.get('user', '')
    guest_list = Guest.objects.all()
    #创建每页3条数据的分页器
    paginator = Paginator(guest_list,3)
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        #如果page不是整数,取第一页面数据
        contacts = paginator.page(1)
    except EmptyPage:
        #如果page不在范围，取最后一页面
        contacts = paginator.page(paginator.num_pages)

    return render(request,'guest_manage.html',{"user":username,"guests":contacts})

#发布会页面的搜索按钮

def search_name(request):
    username = request.session.get('user','')
    search_name = request.GET.get("name","")
    event_list = Event.objects.filter(name__contains=search_name)
    return render(request,"event_manage.html",{"user":username,"events":event_list})

#嘉宾页的搜索按钮

def search_phone(request):
    username = request.session.get('user','')
    search_phone = request.GET.get("phone","")
    guest_list = Guest.objects.filter(phone__contains=search_phone)
    return render(request,"guest_manage.html",{"user":username,"guests":guest_list})

#签到页面

def sign_index(request,event_id):
    event = get_object_or_404(Event,id=event_id)
    return render(request,'sign_index.html',{'event':event})

#输入手机号,点击签到按钮后
def sign_index_action(request,event_id):
    event = get_object_or_404(Event, id=event_id)
    phone = request.POST.get('phone','')
    print('phone===============',phone)

    #查询手机号在Guest表中是否存在,如果不存在提示用户"phone error"
    result = Guest.objects.filter(phone=phone)
    if not result:
        return render(request,"sign_index.html",{'event':event,'hint':'电话号码错误'})

    #通过手机号和发布会id两个条件来查询Guest表,结果为空,则说明手机号与发布会不匹配,提示用户发布会或者手机号错误
    result = Guest.objects.filter(phone=phone,event_id = event_id)
    if not result:
        return render(request,"sign_index.html",{'event':event,'hint':'发布会或者手机号错误'})
    #判断状态是否为true,1是ture,如果为true,则表示嘉宾已签到过了,提示用户已签到,否则说明嘉宾未签到,修改状态为1,提示用户签到成功
    #并显示嘉宾签到成功
    result = Guest.objects.get(phone=phone,event_id=event_id)
    if result.sign:
        return render(request,"sign_index.html",{'event':event,'hint':'用户已签到'})
    else:
        Guest.objects.filter(phone=phone,event_id=event_id).update(sign='1')
        return render(request,'sign_index.html',{'event':event,'hint':"签到成功",'guest':result})

# 退出登录函数
def logout(request):
    response = HttpResponseRedirect('/index/')
    return response