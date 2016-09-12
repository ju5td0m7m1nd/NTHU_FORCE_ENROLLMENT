from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect,HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
import sys
import os
import re

import Choose_lecture
import pickle
import requests
import urllib
from django.http import JsonResponse
from Main.models import *
from collections import Counter

# Create your views here.

def main (request):
  s = requests.Session()
  request.session['s'] = s
  get_captcha(request)
  return render_to_response('index.html',RequestContext(request,locals()))

@csrf_exempt
def query (request):
  query = request.POST.get('query')
  
  return JsonResponse({'data':[]})

@csrf_exempt
def choose_lecture(request):
  account = request.POST.get('account')
  password = request.POST.get('password')
  auth_num = request.POST.get('auth_num')
  course_id = request.POST.get('course_id')
  real = request.POST.get('real')
  print "Views: data fetch success"
  result = Choose_lecture.run(request.session['s_get'],
    request.session['s'],
    account,
    password,
    auth_num,
    course_id,
    real
  )
  return JsonResponse({'result': result})
def get_captcha (request):
  
  s_get = request.session['s'].get('https://www.ccxp.nthu.edu.tw/ccxp/INQUIRE/index.php')
  request.session['s_get'] = s_get
  captcha_num = Choose_lecture.captcha(s_get) 
  return JsonResponse({'captcha': captcha_num})

def get_course(request):
  objects = []
  with (open("./Main/course.p", "rb")) as openfile:
    while True:
        try:
            tmp = pickle.load(openfile)
            objects.append(tmp)
        except EOFError:
            break 
  return JsonResponse({'courses': objects})
