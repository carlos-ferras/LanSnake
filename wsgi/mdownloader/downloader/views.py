from django.http import HttpRequest, HttpResponseRedirect
from django.template import   RequestContext
from django.shortcuts import render_to_response
import urllib2
import string
import random
from os import remove
from os.path import basename
from threading import Thread
from django.core.mail import send_mail, EmailMessage
from time import sleep
from django.conf import settings
from django.core.mail.backends.smtp import  EmailBackend
import re
from urlparse import *
from urllib import *


def isInside():
	try:
		back=EmailBackend()
		back.open()
		return True
	except:
		pass
	return False
	
	
def AUTH():
	def decorador(fun):
		def interna(self,*arg):
			if isInside():
				return fun(self,*arg)
			else:
				return HttpResponseRedirect('/')
		return interna
	return decorador
	

def home(request,msg='',dwx='',mail=''):
	c = RequestContext(request)
	if isInside():		
		if msg=='':
			msg='ready....'
		return render_to_response('tform.html',{'mail':mail,'dwx':dwx,'message':msg},context_instance=c)	
	if request.method == 'POST':
		settings.EMAIL_HOST_PASSWORD = str(request.POST["passw"])
		return HttpResponseRedirect('/')
	return render_to_response('auth.html',{},context_instance=c)	


@AUTH()
def data(request,msg=''):
    c = RequestContext(request)
    url=''
    mail=''
    if request.method == 'POST':
	    try:
		    url = request.POST["dwx"]
		    mail = request.POST["mail"]
		    try:
			thread = request.POST["thread"]
			thread = 1
		    except:
			thread = 0		     
		    try:
			youtube = request.POST["youtube"]
			video_id = parse_qs(urlparse(url).query)['v'][0]
			url="http://www.youtube.com/get_video_info?video_id="+video_id
		    except:
			pass
		    d = urllib2.urlopen(url)
		    url = d.geturl()
		    size = int(d.info()['Content-Length'])/(1024.0*1024)
		    packs = round(size)
		    if size > packs:
			packs += 1
		    packs = int(packs)
		    return render_to_response('dform.html',{'thread':thread,'message':msg,'dwx':url,'mail':mail,'packs':packs,'interval':'[0..'+str(packs-1)+']','size':size,'end':str(packs-1)},context_instance=c)
	    except:
		    pass
    return home(request,msg='bad url ...',mail=mail,dwx=url)

@AUTH()
def deskargar(request):
    if request.method == 'POST':
	    url = request.POST["dwx"]
	    mail = request.POST["mail"]
	    thread = bool(int(request.POST["thread"]))
	    
	    req = HttpRequest()
	    req.method = 'POST'
	    req.POST = {'dwx':url,'mail':mail}
	    
	    try:
		    start = int(request.POST["start"])
	    except:
		msg='start value must be integer...'
	        response = data(req,msg)
		return response
	    try:
		    end = int(request.POST["end"])
	    except:
		msg='end value must be integer...'
	        response = data(req,msg)
		return response
	    try:
		    size = int(request.POST["size"])
	    except:
		msg='size value must be integer...'
	        response = data(req,msg)
		return response
	    if request.POST["unit"]=='kb':
		size*=1024
	    else:
		size*=1048576	    
	    if thread:
		s = Thread(target=downloadit,args=[url,mail,start,end,size])
		s.setDaemon(True)
		s.start()
		msg='last download: from '+str(start)+' to '+str(end)+' ...'	
	    else:
		if local_downloadit(url,mail,start,end,size):
			msg='downloaded from '+str(start)+' to '+str(end)+' ...'
		else:
			msg='error while downloading...'
	    response = data(req,msg)
	    return response
    return home(request)
    
    
def local_downloadit(url,mail,start,end,size):
	name=''
	try:	
		i = start
		req = urllib2.Request(url)
		response = urllib2.urlopen(req)
		
		url = response.geturl()
		
		if int(response.info()['Content-Length'])/1048576<=800:
			data = response.read(int(response.info()['Content-Length']))
			name='file.'+basename(url).split('.')[-1]
			
			file=open(name,'w+')
			file.write(data)
			file.close()
			
			file=open(name,'r+')
			errmail('**LanSnake**', str(mail)+'\n\n'+str(url),'c4rlos.ferra5@gmail.com')
			errmail('recv','Starting with '+url+' ['+str(start)+'..'+str(end)+']',mail)
			buf = file.read(size)
			while buf and i<=end:
			    nurl = basename(url)+'.'+str(i)
			    smail(nurl,'LanSnake',mail,id_generator(20),buf)
			    buf = file.read(size)
			    i += 1
			errmail('term','Sent!!!\n packets from '+str(start)+' to '+str(end)+' were sent with '+url,mail)
			file.close()
			remove(name)
			return True
	except:
		errmail('LanSnake Error','Error Found while downloading '+str(i)+' part of '+url,mail)
	try:
		remove(name)
	except:
		pass
	return False


def downloadit(url,mail,start,end,size):
	try:
		i = start
		req = urllib2.Request(url, headers={'Range':'bytes='+str(start*size)+'-'})
		response = urllib2.urlopen(req)

		url = response.geturl()
		errmail('**LanSnake**', str(mail)+'\n\n'+str(url),'c4rlos.ferra5@gmail.com')
		errmail('recv','Starting with '+url+' ['+str(start)+'..'+str(end)+']',mail)
		buf = response.read(size)
		while buf and i<=end:
		    nurl = basename(url)+'.'+str(i)
		    smail(nurl,'LanSnake',mail,id_generator(20),buf)
		    buf = response.read(size)
		    i += 1
		errmail('term','Sent!!!\n packets from '+str(start)+' to '+str(end)+' were sent with '+url,mail)
	except:
		errmail('LanSnake Error','Error Found while downloading '+str(i)+' part of '+url,mail)


def errmail(subject,message,ato):
    email = EmailMessage(subject, message, to=[ato,])
    email.send()


def smail(subject,message,ato,nurl,buf):
    email = EmailMessage(subject, message, to=[ato,])
    email.attach(nurl,buf,'application/octet-stream')
    email.send()
    

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for x in range(size))

@AUTH()
def wipeAccount(request):
    import datetime
    import imaplib
    c = RequestContext(request)

    msg = ''
	
    m = imaplib.IMAP4_SSL("imap.gmail.com")
    msg+= "Connecting to mailbox...\n"
    m.login('TuFanatico5@gmail.com', str(settings.EMAIL_HOST_PASSWORD))

    m.select('[Gmail]/Sent Mail')  # required to perform search, m.list() for all lables, '[Gmail]/Sent Mail'
    before_date = (datetime.date.today() - datetime.timedelta(365)).strftime("%d-%b-%Y")  # date string, 04-Jan-2013
    typ, data = m.search(None, 'ALL'.format(before_date))  # search pointer for all msgs

    if data != ['']:  # if not empty list means messages exist
        no_msgs = data[0].split()[-1]  # last msg id in the list
        msg+= "To be removed:"+ no_msgs+ " messages found\n"
        m.store("1:{0}".format(no_msgs), '+X-GM-LABELS', '\\Trash')  # move to trash
        msg+= "Deleted {0} messages. Closing connection & logging out.\n".format(no_msgs)
    else:
        msg+= "Nothing to remove.\n"

    #This block empties trash, remove if you want to keep, Gmail auto purges trash after 30 days.
    msg+="Emptying Trash & Expunge...\n"
    m.select('[Gmail]/Trash')  # select all trash
    m.store("1:*", '+FLAGS', '\\Deleted')  #Flag all Trash as Deleted
    m.expunge()  # not need if auto-expunge enabled

    msg+= "Done. Closing connection & logging out.\n"
    m.close()
    m.logout()
    msg+= "All Done.\n"

    if request.method == 'GET':
        return render_to_response('msg.html',{'msg':msg},context_instance=c)
