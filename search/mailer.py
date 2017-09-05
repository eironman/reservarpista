from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from smtplib import SMTPException
from core.models import SportsCenter

"""<QueryDict: {'sport': ['Pádel'], 'duration': ['60 minutos'], 'phone': ['9393939'], 'email': ['ashleyriot@hotmail.com'], 
'userName': ['Aaron'], 'location': ['Palma'], 'sportsCenterId': ['74'], 'time': ['Cualquiera']}>
"""


class SearchMailer:
    """Sends the email for the booking request"""

    sports_center = None
    location = None
    user_name = None
    user_phone = None
    user_email = None
    sport = None
    date = None
    time = None
    duration = None
    msg_plain = None
    msg_html = None
    email_to = None
    subject = None
    email_bcc = None

    def __init__(self, request):
        self.sports_center = SportsCenter.objects.get(id=request.POST['sportsCenterId'], active=True)
        self.user_name = request.POST['userName']
        self.location = request.POST['location']
        self.user_phone = request.POST['phone']
        self.user_email = request.POST['email']
        self.sport = request.POST['sport']
        self.date = request.POST['date']
        self.time = request.POST['time']
        self.duration = request.POST['duration']

    def send_request(self):
        """Sends the booking request to the sports center"""

        email_data = {
            'sports_center_name': self.sports_center.name,
            'name': self.user_name,
            'sport': self.sport,
            'date': self.date,
            'time': self.time,
            'duration': self.duration,
            'email': self.user_email,
            'phone': self.user_phone,
        }
        self.msg_plain = render_to_string('email/booking_request.txt', email_data)
        self.msg_html = render_to_string('email/booking_request.html', email_data)
        self.subject = 'Solicitud de Reserva'

        emails_sent = True

        # Email to sports center
        self.email_to = self.sports_center.email
        if not self.__send_email():
            emails_sent = False

        # Email to me
        self.email_to = 'info@reservarpista.es'
        if not self.__send_email():
            emails_sent = False

        # Email to user
        if not self.user_email == '':
            self.email_to = self.user_email
            if not self.__send_email():
                emails_sent = False

        return emails_sent

    def __send_email(self):
        email = EmailMultiAlternatives(
            '[Reservar Pista] ' + self.subject,
            self.msg_plain,
            'info@reservarpista.es',
            [self.email_to]
        )

        if self.email_bcc:
            email.bcc = self.email_bcc

        if self.msg_html:
            email.attach_alternative(self.msg_html, 'text/html')

        try:
            email.send()
        except SMTPException as e:
            # TODO Register exceptions
            return False

        return True





































