# -*- coding:utf-8  -*-
from urllib2 import urlopen
from pyquery import PyQuery as pq
import getpass
import requests
import os
import io
import chardet
import HTMLParser
import string
import random

def get_auth_num(s_get):
    base_url = 'https://www.ccxp.nthu.edu.tw/ccxp/INQUIRE/'
    tmp = pq(s_get.text)
    a = pq(tmp('img')[4]).attr('src')
    img_url = base_url + a
    r = requests.get(img_url)
    tmp_r = r.content
    random_number = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(10))
    target = open('./static/captcha/'+ random_number + '.png','w')
    target.write(tmp_r)
    target.close()

    return random_number + '.png'
def loginPage(s_get, s, account, password, auth_num):
    base_url = 'https://www.ccxp.nthu.edu.tw/ccxp/INQUIRE/'
    tmp = pq(s_get.text)
    a = pq(tmp('img')[4]).attr('src')
  
    fnstr = a.split('=')[1]

    data = {
        'account' : account,
        'passwd' : password,
        'fnstr' : fnstr, 
        'passwd2' : auth_num,
        }
    login_result = s.post('https://www.ccxp.nthu.edu.tw/ccxp/INQUIRE/pre_select_entry.php',data)
    print ("Login: post to entry success")
    login_url = login_result.text.split('url=')[1].split('>')[0]
    
    s.get('https://www.ccxp.nthu.edu.tw/ccxp/INQUIRE/' + login_url)  #login
    print ("Login: enter main page success") 
    return login_url
   
    
def get_ACIXSTORE(login_meta):
    print ("login_meta: " + login_meta)
    tmp = login_meta.split('STORE=')[1].split('&')[0]

    return tmp


def  makePOST(ACIX, quit, course_id, real):
    if quit == 1:
        data = {
        'c_key':'10420CS 547000',
        'Submit5':'退QUIT',
        'chkbtn':'quit',
        'ACIXSTORE' :ACIX,
        'auth_num':''
        }
    else :
        data = {
        'ckey': course_id,
        'real': real,
        'cred':'0',
        'chkbtn':'add',
        'ACIXSTORE' :ACIX,
        'auth_num':''
        }
    return data 
        
def AddQuit(data,ACIX,s):
    
    tmp_get = s.post('https://www.ccxp.nthu.edu.tw/ccxp/COURSE/JH/7/7.1/7.1.3/JH7130011.php',data={'ACIXSTORE':ACIX})
    posturl = 'https://www.ccxp.nthu.edu.tw/ccxp/COURSE/JH/7/7.1/7.1.3/JH713005.php?ACIXSTORE='+ACIX+'&ts_pwd=a'
    p = s.post(posturl, data)
    print ("Add: send post success")
    q = p.text
    print ("Add: get response text success")
    try:
            q_e = unicode(q).split("alert('")[1].split("')")[0]
            if 'alert' in unicode(q):
                print  'Failed: ' + q_e.encode('latin1').decode('Big5')
                return  'Failed: ' + q_e.encode('latin1').decode('Big5')
                #AddQuit(data,ACIX,s)
    except:
        try:
            print unicode(q).encode('latin1').decode('Big5')
        except:
            print q
        print 'Something happened'
        return 'success'
    
def Add_Main(course_id, ACIXSTORE, s, real):
    data = makePOST(ACIXSTORE, 0, course_id, real)
    print ("create data success")
    return AddQuit(data,ACIXSTORE,s)

# s for session
def captcha(s_get):
  return get_auth_num(s_get)

def run(s_get, s, account, password, auth_num, course_id, real):        
  # login
  login_meta = loginPage(s_get, s, account, password, auth_num)
  # get acixstore
  ACIXSTORE = get_ACIXSTORE(login_meta)
  result = Add_Main(course_id, ACIXSTORE, s, real)
  s.close()
  return result
