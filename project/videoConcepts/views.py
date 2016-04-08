from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello, world. You're at the videoConcepts index.")
    
def processVideo(request, video_id):
    response = "Processing video %s."
    return HttpResponse(response % video_id)