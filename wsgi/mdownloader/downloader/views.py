from django.http import HttpResponse, HttpResponseRedirect
from django.http import HttpRequest
from django.template import Context, loader, RequestContext
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
import urllib2

import string
import random
from time import sleep
from os.path import basename
from threading import Thread

MAX=0

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for x in range(size))

from django.core.mail import send_mail, EmailMessage


def smail(subject,message,ato,nurl,buf):
    email = EmailMessage(subject, message, to=[ato,])
    email.attach(nurl,buf,'application/octet-stream')
    email.send()

def errmail(subject,message,ato):
    email = EmailMessage(subject, message, to=[ato,])
    email.send()

def testMail():
   print "sending throut gmail"
   username = "TuFanatico5@gmail.com"
   password = "bmfkhmpzitaslgnp"
   fromaddr = "TuFanatico5@gmail.com"
   toaddr = "cmferras@estudiantes.uci.cu"
   msg = "join the quark"

   import smtplib

   server = smtplib.SMTP_SSL('smtp.googlemail.com:465')
   server.login(username, password)
   server.sendmail(fromaddr, [toaddr], msg)
   server.quit()
   print "sended"

m1 = 1024*1024.0


def home(request):
    c = RequestContext(request)
    if request.method == 'GET':
        return render_to_response('tform.html',{'message':'ready....'},context_instance=c)

def downloadit(url,mail,start,end):
	
    #~ if end>MAX:
	#~ end=MAX
    try:
        i = start
        #req = urllib2.Request(url, headers={'Range':'bytes='+str(start*m1)+'-'})
        #response = urllib2.urlopen(req)
	response = urllib2.urlopen(url)
        url = response.geturl()
        errmail('recv','Starting with '+url+'       ['+str(start)+'..'+str(end)+']',mail)
        buf = response.read(m1)
        l = len(buf)	
	
	while i<= end:
            nurl = basename(url)+'.'+str(i)
            smail(nurl,'MDownloader',mail,id_generator(20),buf)
            #errmail('sent','sent '+nurl,mail)
            sleep(0.1)
            buf = response.read(m1)
            i += 1
            l += len(buf)
	errmail('term','Sent!!!\n packets from '+str(start)+' to '+str(end)+' were sent with '+url,mail)
    except:
        errmail('MDownloader Error','Error Found while downloading '+str(i)+' part of '+url,mail)


def deskargar(request):
    req = HttpRequest()
    req.method = 'POST'
    url = request.POST["dwx"]
    mail = request.POST["mail"]
    start = int(request.POST["start"])
    end = int(request.POST["end"])

    s = Thread(target=downloadit,args=[url,mail,start,end,])
    s.setDaemon(True)
    s.start()

    req.POST = {'dwx':url,'mail':mail}
    response = downloaded(req)
    return response


def downloaded(request):
    c = RequestContext(request)
#    try:
    url = request.POST["dwx"]
    mail = request.POST["mail"]

    d = urllib2.urlopen(url)
    url = d.geturl()
    size = int(d.info()['Content-Length'])/m1
    packs = round(size)
    if size > packs:
        packs += 1
    packs = int(packs)
    MAX=packs-1
    #errmail('MDownloader Information','You are about to download '+url+'. This is an advice message.',mail)
    return render_to_response('dform.html',{'dwx':url,'mail':mail,'packs':packs,'interval':'[0..'+str(MAX)+']','size':size},context_instance=c)

#    except:
#        return render_to_response('tform.html',{'message':'Error downloading '+url},context_instance=c)

    #return render_to_response('tform.html',{'message':'downloading> '+url+' and sending it to '+mail},context_instance=c)
    return HttpResponseRedirect(reverse('downloader.views.home'))

def wipeAccount(request):
    import datetime
    import imaplib
    c = RequestContext(request)

    msg = ''

    m = imaplib.IMAP4_SSL("imap.gmail.com")  # server to connect to
    msg+= "Connecting to mailbox...\n"
    m.login('TuFanatico5@gmail.com', 'bmfkhmpzitaslgnp')

    m.select('[Gmail]/Sent Mail')  # required to perform search, m.list() for all lables, '[Gmail]/Sent Mail'
    before_date = (datetime.date.today() - datetime.timedelta(365)).strftime("%d-%b-%Y")  # date string, 04-Jan-2013
    #typ, data = m.search(None, '(BEFORE {0})'.format(before_date))  # search pointer for msgs before before_date
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
