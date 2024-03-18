import datetime
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from news.models import Story
import json


@csrf_exempt
def login_user(request):
    if request.method == "POST":
        # get form credentials
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # check if username and password are not empty
        if not username or not password:
            return HttpResponseBadRequest("Username and password are required", status=400)
        
        # authenticate user
        user = authenticate(username=username, password=password)
        
        # login user if authenticated
        if user is not None:
            login(request, user)
            return HttpResponse("Login successful!", status=200)
        else:
            # return 401 if user is not authenticated
            return HttpResponseBadRequest("Invalid username or password", status=401)
    
    return HttpResponseBadRequest("Only POST requests are allowed", status=503)

@csrf_exempt
@login_required
def logout_user(request):
    if request.method == "POST":
        # ensure user is logged in
        if not request.user.is_authenticated:
            return HttpResponseBadRequest("User is not logged in", status=503)
        # logout user
        logout(request)
        return HttpResponse("Logout successful", status=200)
    

@csrf_exempt
def stories(request):

    if request.method == "POST":
        # ensure user is logged in
        if not request.user.is_authenticated:
            return HttpResponseBadRequest("User is not logged in", status=503)
        
        # get form data from json payload
        json_data = json.loads(request.body)
        headline = json_data.get('headline')
        category = json_data.get('category')
        region = json_data.get('region')
        details = json_data.get('details')
        
        # check if headline, category, region and details are not empty
        if not headline or not category or not region or not details:
            return HttpResponseBadRequest("Headline, category, region and details are required", status=503)
        
        # check region and category are valid choices
        if category not in dict(Story._meta.get_field('category').flatchoices):
            return HttpResponseBadRequest("Invalid category", status=503)
        if region not in dict(Story._meta.get_field('region').flatchoices):
            return HttpResponseBadRequest("Invalid region", status=503)
        
        # create story
        story = Story(headline=headline, category=category, region=region, details=details, pub_date=datetime.date.today(), author=request.user.author)
        story.save()
            
        return HttpResponse("Story posted", status=201)
        
        

    elif request.method == "GET":
        # get category region and date from form payload
        category = request.GET.get('category')
        region = request.GET.get('region')
        date = request.GET.get('date')
        
        # get stories
        stories = Story.objects.all()
        return render(request, 'stories.html', {'stories': stories}, status=200)
    
    return HttpResponseBadRequest("Only GET and POST requests are allowed", status=503)
