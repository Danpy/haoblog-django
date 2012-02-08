#coding=utf8

from django.shortcuts import redirect, render_to_response

def test(request):
    return render_to_response('../templates/test.html', {})
