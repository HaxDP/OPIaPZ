from django.http import HttpResponseForbidden
from django.utils.deprecation import MiddlewareMixin


class requestMessageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        print(f"запит: {request.method} {request.path}")
        response = self.get_response(request)
        print(f"відповідь: {response.status_code}")
        return response


class requestContextMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.studentName = "student"
        request.middlewareMessage = "дані добавлено через middleware"
        return self.get_response(request)


class blockPostMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method == "POST" and request.path.startswith("/blocked"):
            return HttpResponseForbidden("POST запити на цю адресу заблоковано")
        return self.get_response(request)


class simpleHeaderMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        response["X-Lab-Name"] = "lab30"
        return response