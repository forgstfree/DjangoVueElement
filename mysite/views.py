from django.http import HttpResponse


def hellp(requset):
    return HttpResponse("Hello world")
