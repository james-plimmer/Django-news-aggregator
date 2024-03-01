from datetime import timezone
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from models import Story

def login(request):
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
            return HttpResponse("Login successful", status=200)
        else:
            # return 401 if user is not authenticated
            return HttpResponseBadRequest("Invalid username or password", status=401)

# can only log out if logged in
@login_required
def logout(request):
    if request.method == "POST":
        # logout user
        logout(request)
        return HttpResponse("Logout successful", status=200)
    
    
def stories(request):
    if request.method == "POST":
        # get form data from json payload
        headline = request.POST.get('headline')
        category = request.POST.get('category')
        region = request.POST.get('region')
        details = request.POST.get('details')
        
        # check if headline, category, region and details are not empty
        if not headline or not category or not region or not details:
            return HttpResponseBadRequest("Headline, category, region and details are required", status=503)
        
        # check if user is logged in
        if request.user.is_authenticated:
            # create story
            story = Story(headline=headline, category=category, region=region, details=details, date_published=timezone.now(), author=request.user.author)
            story.save()
            
            return HttpResponse("Story posted", status=201)
        
        return HttpResponseBadRequest("User is not logged in", status=503)

    elif request.method == "GET":
        # get category region and date from form payload
        category = request.GET.get('category')
        region = request.GET.get('region')
        date = request.GET.get('date')
        
        # get stories
        stories = Story.objects.all()
        return render(request, 'stories.html', {'stories': stories}, status=200)
    
    return HttpResponseBadRequest("Only GET and POST requests are allowed", status=503)
