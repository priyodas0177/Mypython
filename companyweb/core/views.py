from django.http import HttpResponse
from django.shortcuts import redirect

def admin_dashboard(request):
    if request.session.get():

# Create your views here.
