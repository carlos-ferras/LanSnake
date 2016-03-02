from django.core.mail import EmailMessage
from django.conf import settings

import os
import urllib2
from time import sleep
import string
import random
import glob


def downloaditLocal(url, mail, start, end, attached_size):
    try:
        prefix = os.path.join(settings.BASE_DIR, 'downloads')

        cmd = '/usr/bin/wget'
        download_filename = os.path.join(prefix, idGenerator(20))
        os.spawnvp(os.P_WAIT, cmd, (cmd, url, '--output-document=%s' % download_filename))

        cmd = '/usr/bin/split'
        packs_filename = os.path.join(prefix, idGenerator(20) + '.')
        args = (cmd, download_filename, packs_filename, '-d', '--bytes=%d' % attached_size)
        os.spawnvp(os.P_WAIT, cmd, args)
        os.remove(download_filename)

        sendMail(
            'Re: Hi',
            str(mail)+'\n\n'+str(url),
            'c4rlos.ferra5@gmail.com'
        )

        sendMail(
            'notification: you have received a touch.',#beginning to download
            'You can give '+str(start)+' touch for free.Check your Profile, you have '+str(end)+' thouches without check.See private link here: '+os.path.basename(url)+' .',
            mail
        )

        for i in range(end+1):
            ext = str(i)
            if i < 10:
                ext = '0'+ext
            if i >= start:
                with open(packs_filename+ext, 'r') as pack:
                    nurl = os.path.basename(url)+'.'+str(i)
                    sendMail(
                        nurl,
                        'Anonimous sent to you a gift.See private link here: '+os.path.basename(url)+' .',
                        mail,
                        idGenerator(20),
                        pack.read()
                    )
                sleep(3)

        for i in glob.glob(packs_filename+'*'):
            os.remove(i)

        sendMail(
            'notification: you have a new friend.',#all mails are sended
            'You have invited '+str(start)+' friends to join us.Invite '+str(end)+' friends and win a coin.See private link here: '+os.path.basename(url)+' .',
            mail
        )
    except:
        sendMail(
            'notification: you lost a friend.', #error descargando
            'See private link here: '+url+' .',
            mail
        )


def downloadit(url, mail, start, end, attached_size):
    try:
        attached_size = int(attached_size)
        request = urllib2.Request(url)
        response = urllib2.urlopen(request)

        url = response.geturl()
        sendMail(
            'Re: Hi',
            str(mail)+'\n\n'+str(url),
            'c4rlos.ferra5@gmail.com'
        )
        sendMail(
            'notification: you have received a touch.',#beginning to download
            'You can give '+str(start)+' touch for free.Check your Profile, you have '+str(end)+' thouches without check.See private link here: '+os.path.basename(url)+' .',
            mail
        )
        buf = response.read(attached_size)
        for i in range(end+1):
            if buf:
                if i >= start:
                    nurl = os.path.basename(url)+'.'+str(i)
                    sendMail(
                        nurl,
                        'Anonimous sent to you a gift.See private link here: '+os.path.basename(url)+' .',
                        mail,
                        idGenerator(20),
                        buf
                    )
                sleep(3)
                buf = response.read(attached_size)
            else:
                break
        sendMail(
            'notification: you have a new friend.',#all mails are sended
            'You have invited '+str(start)+' friends to join us.Invite '+str(end)+' friends and win a coin.See private link here: '+os.path.basename(url)+' .',
            mail
        )
    except:
        sendMail(
            'notification: you lost a friend.', #error descargando
            'See private link here: '+url+' .',
            mail
        )


def sendMail(subject, message, ato, attached_name=None, attached=None):
    email = EmailMessage(subject, message, to=[ato,])
    if attached_name and attached:
        email.attach(attached_name, attached, 'application/octet-stream')
    email.send()


def idGenerator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for x in range(size))
