from django.shortcuts import render

from .models import LoginAttempt

# Create your views here.

def login(request):
    # if request.method == 'POST':
    #     username = request.POST.get('username')
    #     password = request.POST.get('password')
    #     print(username,password)

    # if request.method == 'POST':
    #     username = request.POST.get('username')
    #     password = request.POST.get('password')
    #     LoginAttempt.objects.create(
    #         username=username,
    #         password=password
    #     )    

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username,password)

    return render(request, 'login.html')