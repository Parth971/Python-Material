from django.shortcuts import HttpResponse



def home(request):
    print('This is view called')
    return HttpResponse('This is Home Page')

def exception(request):
    print('This is exception view called')
    x = 10/0
    return HttpResponse('This is exception')