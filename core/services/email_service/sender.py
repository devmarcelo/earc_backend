from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings

def send_html_email(subject, to_email, template_name, context, from_email=None):
    html_content = render_to_string(template_name, context)
    from_email = from_email or settings.DEFAULT_FROM_EMAIL
    msg = EmailMultiAlternatives(subject, "", from_email, [to_email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()
