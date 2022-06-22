from celery import shared_task
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.core.mail import send_mail

from time import sleep


@shared_task
def test_task():
    with open('file2.txt', 'w') as file:
        file.write('LogStartWork?     ')
        sleep(60)
        file.write('LogEndWork')
    """with open('file.txt', 'w') as file:
        file.write('LogStart')
        #sleep(10)
        file.write('LogEnd')"""

    return None
