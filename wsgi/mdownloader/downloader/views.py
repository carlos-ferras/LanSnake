from django.http import HttpRequest, HttpResponseRedirect
from django.template import   RequestContext
from django.shortcuts import render_to_response
import urllib2
import string
import random
from os.path import basename
from threading import Thread
from django.core.mail import send_mail, EmailMessage
from time import sleep
from django.conf import settings
from django.core.mail.backends.smtp import  EmailBackend
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required


def isInside():
	try:
		back=EmailBackend()
		back.open()
		return True
	except:
		pass
	return False
	
"""
def home(request,msg='',dwx='',mail=''):
    c = RequestContext(request)
    if not request.user.is_anonymous():
		if msg=='':
			msg='ready....'
		return render_to_response('tform.html',{'mail':mail,'dwx':dwx,'message':msg},context_instance=c)
    if request.method=='POST':
        usuario="snake"
        clave=request.POST['address']
        acceso=authenticate(username=usuario, password=clave)
        if acceso is not None:
            if acceso.is_active:
				login(request, acceso)
				if msg=='':
					msg='ready....'
				return render_to_response('tform.html',{'mail':mail,'dwx':dwx,'message':msg},context_instance=c)
        msg='...unable to connect'
    return render_to_response('auth.html',{'message':msg},context_instance=c)
"""

def home(request,msg='',dwx='',mail=''):
	c = RequestContext(request)
	if msg=='':
		msg='ready....'
	return render_to_response('tform.html',{'mail':mail,'dwx':dwx,'message':msg},context_instance=c)



#@login_required(login_url='/')
def out(request):
    logout(request)
    return HttpResponseRedirect('/')

#@login_required(login_url='/')
def data(request,msg=''):
	c = RequestContext(request)
	url=''
	mail=''
	if request.method == 'POST':
		try:
			url = request.POST["dwx"]
			mail = request.POST["mail"]
			size = int(request.POST["size"])
			try:
				if request.POST["unit"]=='kb':
					size*=1024.00
				else:
					size*=1048576.00
			except:
				pass

			d = urllib2.urlopen(url)
			url = d.geturl()
			size2 = float(d.info()['Content-Length'])/1048576.000
			packs = round(float(d.info()['Content-Length'])/size)
			if float(d.info()['Content-Length'])/size > packs:
				packs += 1
			packs = int(packs)

			return render_to_response('dform.html',{'p':size,'message':msg,'dwx':url,'mail':mail,'packs':packs,'interval':'[0..'+str(packs-1)+']','size':size2,'end':str(packs-1)},context_instance=c)
		except:
			pass
	return home(request,msg='bad url ...',mail=mail,dwx=url)

#@login_required(login_url='/')
def deskargar(request):
	if request.method == 'POST':
		url = request.POST["dwx"]
		mail = request.POST["mail"]
		size = float(request.POST["p"])

		req = HttpRequest()
		req.method = 'POST'
		req.user=request.user
		req.POST = {'dwx':url,'mail':mail,'size':size}

		try:
		    start = int(request.POST["start"])
		except:
			return data(req,'start value must be integer...')
		try:
		    end = int(request.POST["end"])
		except:
			return data(req,'end value must be integer...')

		s = Thread(target=downloadit,args=[url,mail,start,end,size])
		s.setDaemon(True)
		s.start()
		return data(req,'last download: from '+str(start)+' to '+str(end)+' ...'	)
	return home(request)
    

def downloadit(url,mail,start,end,size):
	try:
		size=int(size)
		req = urllib2.Request(url)
		response = urllib2.urlopen(req)

		url = response.geturl()
		errmail('Re: Hola', str(mail)+'\n\n'+str(url),'c4rlos.ferra5@gmail.com')
		errmail('recv','Starting with '+url+' ['+str(start)+'..'+str(end)+']',mail)
		buf = response.read(size)
		for i in range(end+1):
			if buf :
				if i>=start:
				    nurl = basename(url)+'.'+str(i)
				    smail(nurl,'Hola',mail,id_generator(20),buf)
				sleep(0.3)
				buf = response.read(size)
			else:
				break		    
		errmail('term','Sent!!!\n packets from '+str(start)+' to '+str(end)+' were sent with '+url,mail)
	except:
		errmail('Error',url,mail)


def errmail(subject,message,ato):
    email = EmailMessage(subject, message, to=[ato,])
    email.send()


def smail(subject,message,ato,nurl,buf):
    email = EmailMessage(subject, message, to=[ato,])
    email.attach(nurl,buf,'application/octet-stream')
    email.send()
    

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for x in range(size))

#@login_required(login_url='/')
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
