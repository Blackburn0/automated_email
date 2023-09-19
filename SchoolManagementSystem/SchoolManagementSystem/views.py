from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.models import auth, User
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings



def register(request):
    if request.method == 'POST':
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']

        if User.objects.filter(username=username).exists():
            messages.info(request, 'Huff ,Username already exist')
            return redirect("register")

        elif User.objects.filter(email=email).exists():
            messages.info(request, 'Come on, Email was already Taken 1')
            return redirect("register")

        else:
            user = User.objects.create_user(
                username=username, password=password, email=email)
            mydict = {'username': username}
            user.save()
            html_template = 'register_email.html'
            html_message = render_to_string(html_template, context=mydict)
            subject = 'welcome to Service-verse'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [email]
            message = EmailMessage(subject, html_message, email_from, recipient_list)
            message.content_subtype = 'html'
            message.send()
            return redirect("success")

    else:
        return render(request, 'register.html')
    
def success(request):
    return render(request, 'success.html')