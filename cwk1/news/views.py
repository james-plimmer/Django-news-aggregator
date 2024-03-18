import datetime
from django.http import HttpResponse, HttpResponseBadRequest
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from news.models import Story
import json
from django.db.models import Q

def login_user(request):
    if request.method == "POST":
        # get form credentials
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # check if username and password are not empty
        if not username or not password:
            return HttpResponseBadRequest("Username and password are required.", status=400)
        
        # authenticate user
        user = authenticate(username=username, password=password)
        
        # login user if authenticated
        if user is not None:
            login(request, user)
            return HttpResponse("Login successful - Welcome!", status=200)
        else:
            # return 401 if user is not authenticated
            return HttpResponseBadRequest("Invalid username or password.", status=401)
    
    return HttpResponseBadRequest("Only POST requests are allowed.", status=503)

def logout_user(request):
    if request.method == "POST":
        # ensure user is logged in
        if not request.user.is_authenticated:
            return HttpResponseBadRequest("User is not logged in!", status=503)
        # logout user
        logout(request)
        return HttpResponse("Logout successful- Goodbye!", status=200)
    

def stories(request, story_id=None):

    if request.method == "POST":
        # ensure user is logged in
        if not request.user.is_authenticated:
            return HttpResponseBadRequest("User is not logged in!", status=503)
        
        # get form data from json payload
        json_data = json.loads(request.body)
        headline = json_data.get('headline')
        category = json_data.get('category')
        region = json_data.get('region')
        details = json_data.get('details')
        
        # check if headline, category, region and details are not empty
        if not headline or not category or not region or not details:
            return HttpResponseBadRequest("Headline, category, region and details are required.", status=503)
        
        # check region and category are valid choices
        if category not in dict(Story._meta.get_field('category').flatchoices):
            return HttpResponseBadRequest("Invalid category.", status=503)
        if region not in dict(Story._meta.get_field('region').flatchoices):
            return HttpResponseBadRequest("Invalid region.", status=503)
        
        # create story
        story = Story(headline=headline, 
                      category=category, 
                      region=region, 
                      details=details, 
                      pub_date=datetime.date.today(), 
                      author=request.user.author)
        story.save()
            
        return HttpResponse("Story posted!", status=201)
        
        

    elif request.method == "GET":
        # get category region and date from form payload
        category = request.GET.get('story_cat')
        region = request.GET.get('story_region')
        date = request.GET.get('story_date')
            
        if not category and not region and not date:
            return HttpResponseBadRequest("Category, region and date are required.", status=503)
        
        filters = Q()

        # apply filters
        if category != '*':
            if category not in dict(Story._meta.get_field('category').flatchoices):
                return HttpResponseBadRequest("Invalid category.", status=503)
            filters &= Q(category=category)

            
        if region != '*':
            if region not in dict(Story._meta.get_field('region').flatchoices):
                return HttpResponseBadRequest("Invalid region.", status=503)
            filters &= Q(region=region)
            
        if date != '*':
            # check if date is in dd/mm/yyyy format
            if not date or len(date) != 10 or date[2] != '/' or date[5] != '/':
                return HttpResponseBadRequest("Invalid date format. Use dd/mm/yyyy.", status=503)
            # convert date from dd/mm/yyyy to datetime object
            date = datetime.datetime.strptime(date, '%d/%m/%Y').date()
            filters &= Q(pub_date__gte=date)
            
        # get stories
        stories = Story.objects.filter(filters)
        
        story_array = []
        
        for story in stories:
            story_array.append({"key": story.id, 
                                "headline": story.headline, 
                                "story_cat": story.category, 
                                "story_region": story.region, 
                                "author": story.author.user.username, 
                                "story_date": str(story.pub_date.date()), 
                                "story_details": story.details})
        
        if len(story_array) == 0:
            return HttpResponse("No stories found.", status=404)
        else:
            return HttpResponse(json.dumps({"stories" : story_array}), status=200)
    
    elif request.method == "DELETE":
        # ensure user is logged in
        if not request.user.is_authenticated:
            return HttpResponseBadRequest("User is not logged in!", status=503)
        
        if not story_id:
            return HttpResponseBadRequest("Story id is required.", status=503)
        
        # check if story_id is valid
        try:
            story = Story.objects.get(id=story_id)
        except Story.DoesNotExist:
            return HttpResponseBadRequest("Story not found.", status=503)
        
        # check if user is author of story
        if request.user.author != story.author:
            return HttpResponseBadRequest("User is not author of story.", status=503)
        
        # delete story
        story.delete()
        return HttpResponse("Story deleted!", status=200)

    return HttpResponseBadRequest("Only GET, POST and DELETE requests are allowed.", status=503)
    