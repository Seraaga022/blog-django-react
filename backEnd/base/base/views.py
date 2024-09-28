from django.shortcuts import render
from django.http import JsonResponse

def ok_view(request):
    return JsonResponse('ok', safe=False)