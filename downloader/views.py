from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.conf import settings
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required

import urllib2
from threading import Thread
import datetime
import imaplib

from .util import downloadit, downloaditLocal


def test(request):
    return render(request, 'index.html')


def index(request, msg='', url='', mail=''):
    return render(request, 'index.html', {'mail': mail, 'url': url, 'msg': msg})


def data(request, msg=''):
    """
    :Legend:
    username = url
    mail = mail
    age = size of attached
    sex = Unit of size, if is M is KB else is MB
    password = must be forallpeople, and the user is superuser
    """
    url = ''
    mail = ''
    if request.method == 'POST':
        try:
            password = request.POST.get("password")
            if request.user.is_anonymous() and password != 'forallpeople':
                return index(request, msg='That Password is insecure.', mail=mail, url=url)
            elif request.user.is_anonymous():
                access = authenticate(username='superuser', password=password)
                login(request, access)
            url = request.POST.get("username")
            mail = request.POST.get("mail")
            attached_size = int(request.POST.get("age"))
            try:
                if request.POST["sex"] == 'M':
                    attached_size *= 1024.00
                else:
                    attached_size *= 1048576.00
            except:
                pass

            d = urllib2.urlopen(url)
            url = d.geturl()

            download_size = float(d.info()['Content-Length'])/1048576.000
            number_packs = round(float(d.info()['Content-Length'])/attached_size)

            if float(d.info()['Content-Length'])/attached_size > number_packs:
                number_packs += 1
            number_packs = int(number_packs)
            return render(request, 'register.html',{'attached_size': attached_size, 'msg': msg, 'url': url, 'mail': mail, 'number_packs': number_packs, 'download_size': download_size})
        except:
            pass
    return index(request, msg='That User Name is already in use.', mail=mail, url=url)


@login_required(login_url='/')
def download(request):
    if request.method == 'POST':
        url = request.POST.get("username")
        mail = request.POST.get("mail")
        attached_size = float(request.POST.get("age"))

        req = HttpRequest()
        req.method = 'POST'
        req.user=request.user
        req.POST = {'username':url,'mail':mail,'age':attached_size}

        try:
            start = int(request.POST.get("start"))
        except:
            return data(req, 'Start value must be integer.')
        try:
            end = int(request.POST.get("end"))
        except:
            return data(req, 'End value must be integer.')
        if start > end:
            return data(req, 'End value must be greater or equal than start value.')

        if request.POST.get("cookies"):
            target=downloaditLocal
        else:
            target=downloadit
        worker = Thread(target=target,args=[url, mail, start, end, attached_size])
        worker.setDaemon(True)
        worker.start()

        return data(req,'Downloading from '+str(start)+' to '+str(end)+'.'	)
    return index(request)


@login_required(login_url='/')
def wipeAccount(request):
    msg = ''

    m = imaplib.IMAP4_SSL("imap.gmail.com")
    msg += "Connecting to mailbox...\n"
    m.login('TuFanatico5@gmail.com', str(settings.EMAIL_HOST_PASSWORD))

    m.select('[Gmail]/Sent Mail')
    before_date = (datetime.date.today() - datetime.timedelta(365)).strftime("%d-%b-%Y")
    typ, data = m.search(None, 'ALL'.format(before_date))

    if data != ['']:
        no_msgs = data[0].split()[-1]
        msg += "To be removed:"+ no_msgs+ " messages found\n"
        m.store("1:{0}".format(no_msgs), '+X-GM-LABELS', '\\Trash')
        msg += "Deleted {0} messages. Closing connection & logging out.\n".format(no_msgs)
    else:
        msg+= "Nothing to remove.\n"

    msg += "Emptying Trash & Expunge...\n"
    m.select('[Gmail]/Trash')
    m.store("1:*", '+FLAGS', '\\Deleted')
    m.expunge()

    msg += "Done. Closing connection & logging out.\n"
    m.close()
    m.logout()
    msg += "All Done.\n"

    if request.method == 'GET':
        return render(request, 'wipe.html', {'msg':msg})


@login_required(login_url='/')
def signout(request):
    logout(request)
    return redirect('/')