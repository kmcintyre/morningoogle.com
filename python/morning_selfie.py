import StringIO
import os

from email import Encoders
from email.generator import Generator
from email.mime.multipart import MIMEMultipart, MIMEBase
from email.mime.text import MIMEText

from twisted.application import internet
from twisted.internet import protocol
from twisted.mail import smtp, relaymanager
from twisted.python import log


fn = "05 - All These Things That Ive Done.mp3"
multipart = MIMEMultipart('alternative')
multipart['Subject'] = 'All These Things That Ive Done'
multipart['To'] = 'mg@scewpt.com'
multipart['From'] = 'just_me@scewpt.com'

text = "Hello, how are you, goodbye."
textpart = MIMEText(text)
multipart.attach(textpart)
htmlpart = MIMEText("<html>" + text + "</html>", 'html')
multipart.attach(htmlpart)

part = MIMEBase('audio', "mp3")
part.set_payload(open(fn, "rb").read())
Encoders.encode_base64(part)
part.add_header(
    'Content-Disposition', 'attachment; filename="%s"' % os.path.basename(fn))
multipart.attach(part)

io = StringIO.StringIO()
g = Generator(io, False)  # second argument means "should I mangle From?"
g.flatten(multipart)
v = io.getvalue()


class SMTPTutorialClient(smtp.ESMTPClient):
    mailFrom = "selfie@scewpt.com"
    mailTo = "mg@scewpt.com"

    def getMailFrom(self):
        result = self.mailFrom
        self.mailFrom = None
        return result

    def getMailTo(self):
        return [self.mailTo]

    def getMailData(self):
        log.msg('mail data:', v)
        return StringIO.StringIO(v)

    def sentMail(self, code, resp, numOk, addresses, log):
        log.msg('sent', numOk, 'messages', resp)
        from twisted.internet import reactor
        reactor.stop()


class SMTPClientFactory(protocol.ClientFactory):
    protocol = SMTPTutorialClient

    def buildProtocol(self, addr):
        log.msg('buildprotocol')
        return self.protocol(secret=None, identity='scewpt.com')


def getMailExchange(host):
    def cbMX(mxRecord):
        return str(mxRecord.name)
    return relaymanager.MXCalculator().getMX(host).addCallback(cbMX)

if __name__ == '__main__':
    from twisted.internet import reactor

    def cbMailExchange(exchange):
        log.msg('received exchange', exchange)
        smtpClientFactory = SMTPClientFactory()
        smtpClientService = internet.TCPClient(exchange, 25, smtpClientFactory)
        smtpClientService.startService()
    getMailExchange('scewpt.com').addCallback(cbMailExchange)
    reactor.run()
