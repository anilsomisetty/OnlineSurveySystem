# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from survey.models import Survey,questions,approver
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import loader,render,redirect
from .forms import *
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django import forms

sid=0
questionnum=1
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/login')
    else:
        form = SignUpForm()
    return render(request, 'survey/signup.html', {'form': form})

def approverlogin(request):
    if request.method == 'POST':
        form=approverForm(request.POST)
        if form.is_valid():
            username=form.cleaned_data.get('Username')
            password=form.cleaned_data.get('password')
            chec=approver.objects.filter(username=username,password=password).count()
            survey=Survey.objects.all()
            if chec > 0 :
                return redirect('/correct') 
            else:
                return render(request,'survey/wrong.html')
    else:
        form=approverForm
        return render(request,'survey/approverlogin.html',{'form':form})

def correct(request):
    if request.method == 'POST': 
        form=approverForm(request.POST)
        survey=Survey.objects.all()
        return render(request,'survey/approver.html',{'surveys': survey})
    else:
        return render(request,'survey/correct.html')    
def approve(request,sid):
    user=request.user
    username=user.username
    surveys=Survey.objects.get(id=sid)
    surveys.check1='True'
    surveys.save()
    survey=Survey.objects.all()
    return redirect('/correct')

def rejectsurvey(request,sid):
    user=request.user
    username=user.username
    survey=Survey.objects.get(id=sid)
    survey.check3=False
    survey.save()
    survey=Survey.objects.all()
    return render(request,'survey/approver.html',{'surveys': survey,'username':username})
def surveys(request):
    
    if request.method =='POST':
        user=request.user
        form=SurveyForm(request.POST)
        if form.is_valid() and request.user.is_authenticated() :
            global sid
            global questionnum
            surveyname=form.cleaned_data['surveyname']
            surveymessage=form.cleaned_data['surveymessage']
            #numberofquestions=form.cleaned_data['numberofquestions']
            surveys=Survey.objects.create(surveyname=surveyname,surveymessage=surveymessage,userid=user.username,check=False)
            surveys.save()
            iid=Survey.objects.get(userid=user.username,check=False)
            sid=iid.id
            questionnum=1
            # print sid
            iid.check=True
            iid.save()
            # em=user.email
            # email = EmailMessage('SurveyTool', 'You have sucesfully created a survey', to=[em])
            # email.send()
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
            global questionnum
            question=form.cleaned_data['question']
            option1=form.cleaned_data['option1']
            option2=form.cleaned_data['option2']
            option3=form.cleaned_data['option3']
            option4=form.cleaned_data['option4']
            question=questions.objects.create(questionid=questionnum,question=question,option1=option1,option2=option2,option3=option3,option4=option4,yid=sid)
            question.save()
            questionnum=questionnum+1
            # print sid
        return redirect('/%d'%sid)
    else:
        return render(request,'survey/addquestion.html',{'form' : form})
def deletequestion(request,sid,id):
    if request.method=='POST' and request.user.is_authenticated():
        que=questions.objects.get(yid=sid,questionid=id)
        que.delete()
        sid=int(sid)
        # em=user.email
        # email = EmailMessage('SurveyTool', 'You have sucesfully deleted the question in your survey', to=[em])
        # email.send()
        return redirect('/%d'%sid)

def deletesurvey(request,sid):
    if request.method=='POST' and request.user.is_authenticated():
        survey=Survey.objects.get(id=sid)
        survey.delete()
        return redirect('/hissurveys')

def editquestion(request,sid,id):
    ques=questions.objects.get(yid=sid,questionid=id)
    if request.method=="POST":
        user=request.user
        form=questionForm(request.POST)
        if form.is_valid() and request.user.is_authenticated():    
            question=form.cleaned_data['question']
            option1=form.cleaned_data['option1']
            option2=form.cleaned_data['option2']
            option3=form.cleaned_data['option3']
            option4=form.cleaned_data['option4']
            ques.question=question
            ques.option1=option1
            ques.option2=option2
            ques.option3=option3
            ques.option4=option4
            ques.save()
            # em=user.email
            # email = EmailMessage('SurveyTool', 'You have sucesfully edited the question in your survey', to=[em])
            # email.send()
            sid=int(sid)
        return redirect('/%d'%sid)
    else:
        form=questionForm
        form.question=ques.question
        form.option1=ques.option1
        form.option2=ques.option2
        form.option3=ques.option3
        form.option4=ques.option4
        return render(request,'survey/editquestion.html',{'form' : form})

def profile(request):
    return render(request,'survey/profile.html')

@login_required
@transaction.atomic
def update_profile(request):
    if request.method == 'POST':
        user=request.user
        #user_form = UserForm(request.POST, instance=request.user)
        form = ProfileForm(request.POST)
        if form.is_valid():
            first_name=form.cleaned_data['first_name']
            last_name=form.cleaned_data['last_name']
            email=form.cleaned_data['email']
            u=User.objects.get(username=user.username)
            u.first_name=first_name
            u.last_name=last_name
            u.email=email
            u.save()            
            # email1 = EmailMessage('SurveyTool', 'You have sucesfully updated your profile', to=[email])
            # email1.send()
            #messages.success(request, _('Your profile was successfully updated!'))
            return redirect('/profile')
        else:
            messages.error(request, _('Please correct the error below.'))
    else:
        #user_form = UserForm(instance=request.user)
        profile_form = ProfileForm
    return render(request, 'survey/update_profile.html', {
       # 'user_form': user_form,
        'profile_form': profile_form
    })

def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            # em=user.email
            # email = EmailMessage('SurveyTool', 'You have sucesfully changed your password', to=[em])
            # email.send()
            return redirect('change_password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'survey/update_password.html', {
        'form': form
    }) 

def showsurveys(request):
    user=request.user
    username=user.username
    survey_num=Survey.objects.filter(userid=username).count()
    survey=Survey.objects.all()
    if survey_num > 0:
        return render(request,'survey/show_surveys.html',{'surveys': survey,'username':username})
    else:
        msg='No surveys found'
        return render(request,'survey/show_surveys.html',{'msg':msg})   

def hissurveys(request):
    user=request.user
    username=user.username
    survey_num=Survey.objects.filter(userid=username).count()
    survey=Survey.objects.all()
    if survey_num > 0 and request.user.is_authenticated() :
        return render(request,'survey/hissurveys.html',{'surveys': survey,'username':username})
    else:
        msg='No surveys found'
        return render(request,'survey/hissurveys.html',{'msg':msg}) 

def getresults(request,sid):
    user=request.user
    username=user.username
    survey=questions.objects.filter(yid=sid)
    return render(request,'survey/results.html',{'questions':survey,'username':username})

def cancelsurvey(request,sid):
    survey=Survey.objects.get(id=sid)
    if survey.check2 :
        survey.delete()
    else :
        survey.check2=True
        survey.delete()
    return redirect('/hissurveys')

