import json
from datetime import datetime
from .models import Story, Author

from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.core.serializers import serialize

# Create your views here.

# login
@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:    # user found
            login(request, user)
            return HttpResponse("Welcome, you are now logged in.", status=200)
        else:   # user not found
            return HttpResponse("Login failed. Please check your username and password.", status=401)
    return HttpResponse("This endpoint only supports POST requests.", status=405)

# logout
@csrf_exempt
def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return HttpResponse("Goodbye, you are now logged out.", status=200)
    return HttpResponse("This endpoint only supports POST requests.", status=405)

# post and get story
@csrf_exempt
@require_http_methods(["POST", "GET"])
def story(request):
    if request.method == "POST":    # for posting story
        if not request.user.is_authenticated:
            return HttpResponse("Authentication required to post stories.", status=503)   
        try:
            data = json.loads(request.body) # load json data from body
            # extract story details
            headline = data.get('headline')
            category = data.get('category')
            region = data.get('region')
            details = data.get('details')
            author = Author.objects.get(user=request.user)  # get author object

            # create new story instance and save
            new_story = Story(headline=headline, category=category, region=region, details=details, author=author)
            new_story.save()
            
            return HttpResponse("Story posted successfully.", status=201)
        except Exception as e:
            return HttpResponse(f"Error posting story: {str(e)}", status=503)
    
    elif request.method == "GET":   # for getting story
        story_cat = request.GET.get('story_cat', '*')
        story_region = request.GET.get('story_region', '*')
        story_date = request.GET.get('story_date', '*')

        stories = Story.objects.all()   # filter stories based on parameter
    
        if story_cat != '*':
            stories = stories.filter(category=story_cat)
        if story_region != '*':
            stories = stories.filter(region=story_region)
        if story_date != '*':
            try:
                date_filter = datetime.strptime(story_date, '%d/%m/%Y').date()
                stories = stories.filter(date__gte=date_filter)
            except ValueError:
                return HttpResponse("Invalid date format. Please use DD/MM/YYYY.", status=400)

        if stories.exists():    # if story exist
            stories_data = json.loads(serialize('json', stories))
            stories_list = [{
                "key": story["pk"],
                "headline": story["fields"]["headline"],
                "story_cat": story["fields"]["category"],
                "story_region": story["fields"]["region"],
                "author": Story.objects.get(id=story["pk"]).author.name,
                "story_date": story["fields"]["date"],
                "story_details": story["fields"]["details"]
            } for story in stories_data]   
            return JsonResponse({"stories": stories_list}, safe=False, status=200) 
        else:
            return HttpResponse("No stories found matching the criteria.", status=404)
    
@csrf_exempt
@require_http_methods(["DELETE"])
def delete_story(request, story_key):
    if not request.user.is_authenticated:
        return HttpResponse("Authentication required to delete stories.", status=503)
    
    try:
        story = Story.objects.get(pk=story_key)
        if story.author.user != request.user: # check if logged-in user is the author
            return HttpResponse("You can only delete stories you've posted.", status=403)
        
        story.delete()
        return HttpResponse("Story deleted successfully.", status=200)
    except Story.DoesNotExist:
        return HttpResponse("Story not found.", status=404)
    except Exception as e:
        return HttpResponse(f"Error deleting story: {str(e)}", status=503)