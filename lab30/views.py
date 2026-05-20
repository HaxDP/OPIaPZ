from django.http import HttpResponse


def indexView(request):
    studentName = getattr(request, "studentName", "невідомо")
    message = getattr(request, "middlewareMessage", "middleware не добавив дані")
    return HttpResponse(f"Привіт, {studentName}. {message}")


def blockedView(request):
    return HttpResponse("GET запит пройшов, але POST буде заблокований")