from django.shortcuts import HttpResponse


def test_middleware(get_response):
    print('One time Initialization - test_middleware')

    def my_function(request):
        print('Before view called - test_middleware')
        response = get_response(request)
        print('Before view called - test_middleware')
        return response

    return my_function


class FatherMiddleware():
    def __init__(self, get_response):
        self.get_response = get_response
        print('One time Execute - FatherMiddleware')

    def __call__(self, request):
        print('Before view called - FatherMiddleware')
        # response = self.get_response(request)
        response = HttpResponse('Returned from FatherMiddleware')
        print('Before view called - FatherMiddleware')
        return response

class MotherMiddleware():
    def __init__(self, get_response):
        self.get_response = get_response
        print('One time Execute - MotherMiddleware')

    def __call__(self, request):
        print('Before view called - MotherMiddleware')
        response = self.get_response(request)
        print('Before view called - MotherMiddleware')
        return response


class ProcessMiddleware():
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, *args, **kwargs):
        print('This is process view before view called')
        # return HttpResponse('This is just before View')
        # if none returned then continue to call view
        return None

class ExceptionMiddleware():
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        print('This is exception view before view called')
        return HttpResponse(exception)