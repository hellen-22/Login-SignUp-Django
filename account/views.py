from django.shortcuts import redirect, render
from django.core.mail import EmailMessage
from django.conf import settings
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.models import auth
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from django.db import transaction
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from django.views import View


from account.models import CustomUser
from account.utils import account_activation_token

# Create your views here.
@transaction.atomic
def signup(request):
    if request.method == "POST":
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirm_password = request.POST["confirm_password"]

        if password == confirm_password:
            if CustomUser.objects.filter(username=username).exists():
                messages.info(request, "Username is Already Taken")
                return redirect("signup")
            elif CustomUser.objects.filter(email=email).exists():
                messages.info(request, "Email Already exists")
                return redirect("signup")
            else:
                user = CustomUser.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email, password=password)

                current_site = get_current_site(request)
                mail_subject = "Account Activation"
                message = render_to_string("activation/activate.html",{
                    "user": user,
                    "domain": current_site.domain,
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "token": account_activation_token.make_token(user)
                })

                email_message = EmailMessage(
                    mail_subject,
                    message,
                    settings.EMAIL_HOST_USER,
                    [email]
                )

                email_message.send()
                
                return render(request, "activation/message.html")

        else:
            messages.info(request, "Password Does Not Match")
            return redirect("signup")
    return render(request, "account/signup.html")

def login(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]

        user = auth.authenticate(email=email, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect("users")

    else:
        return render(request, "account/login.html")

def users(request):
    #response = requests.get("http://127.0.0.1:8000/auth/users/")
    #users = response.json()

    return render(request, "account.html", {"users": users})


class ActivateAccount(View):
    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = CustomUser.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()

            messages.success(request, ("Your account have been confirmed."))
            return redirect("login")
        else:
            messages.warning(request, ("The confirmation link was invalid, possibly because it has already been used."))
            return redirect("signup")



