from django.shortcuts import get_object_or_404, render
from django.core.urlresolvers import reverse

def hello_world(request):
    return render(request, 'index.html')