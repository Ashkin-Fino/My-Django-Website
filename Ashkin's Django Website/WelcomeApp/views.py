from django.http import HttpResponse
from django.shortcuts import render


def welcomePage(request):
    if request.method == 'POST':
        # Get the name from the form
        input = str(request.POST.get('name', ''))
        return render(request, 'welcomeBlock.html', {'name': input})
    elif request.method == 'GET':
        return render(request, "namegetter.html")

