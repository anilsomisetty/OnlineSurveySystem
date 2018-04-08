# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from survey.models import Survey,questions
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import loader,render,redirect
from .forms import *
from django.contrib.auth.models import User


sid=0

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/login')
    else:
        form = UserCreationForm()
    return render(request, 'survey/signin.html', {'form': form})

def surveys(request):
    
    if request.method =='POST':
        user=request.user
        form=SurveyForm(request.POST)
        if form.is_valid() and request.user.is_authenticated() :
            global sid
            surveyname=form.cleaned_data['surveyname']
            surveymessage=form.cleaned_data['surveymessage']
            numberofquestions=form.cleaned_data['numberofquestions']
            surveys=Survey.objects.create(surveyname=surveyname,surveymessage=surveymessage,numberofquestions=numberofquestions,userid=user.username,check=False)
            surveys.save()
            iid=Survey.objects.get(userid=user.username,check=False)
            sid=iid.id
            # print sid
            iid.check=True
            iid.save()
            return redirect('/%d'%sid)
    else:
        form=SurveyForm
    return render(request,'survey/survey.html',{'form' :form})    

def dashboard(request,sid):
    #print sid
    ques_num=questions.objects.filter(yid=sid).count()
    ques=questions.objects.all()
    if ques_num > 0:
        return render(request,'survey/dashboard.html',{'questions': ques,'sid':sid})
    else:
        msg='No questions found'
        return render(request,'survey/dashboard.html',{'msg':msg})
def addquestion(request):
   
    form=questionForm
    if request.method=='POST':
        user=request.user
        form=questionForm(request.POST)
        if form.is_valid() and request.user.is_authenticated():
            global sid
            question=form.cleaned_data['question']
            option1=form.cleaned_data['option1']
            option2=form.cleaned_data['option2']
            option3=form.cleaned_data['option3']
            option4=form.cleaned_data['option4']
            question=questions.objects.create(questionid=1,question=question,option1=option1,option2=option2,option3=option3,option4=option4,yid=sid)
            question.save()
            # print sid
        return redirect('/%d'%sid)
    else:
        return render(request,'survey/addquestion.html',{'form' : form})

