from django import forms
from django.core.exceptions import ValidationError
from accounts.models import User  # Use your actual import path
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from .models import *
from django.contrib.auth import authenticate
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV2Checkbox

from django.contrib.auth import get_user_model
from django.core.mail import EmailMultiAlternatives
from django.template import loader
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes  # Correct import

# rest of the code

from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import default_token_generator
from django.contrib import messages
from django.contrib.auth.backends import ModelBackend
import logging

# Get the custom user model
UserModel = get_user_model()

logger = logging.getLogger(__name__)

class PasswordResetForm(forms.Form):
    email = forms.EmailField(
        label="Email",
        max_length=254,
        widget=forms.EmailInput(attrs={"autocomplete": "email"}),
    )

    def send_mail(
        self,
        subject_template_name,
        email_template_name,
        context,
        from_email,
        to_email,
        html_email_template_name=None,
    ):
        """
        Sends a password reset email to `to_email`.
        """
        subject = loader.render_to_string(subject_template_name, context)
        subject = "".join(subject.splitlines())  # Remove any newlines
        body = loader.render_to_string(email_template_name, context)

        email_message = EmailMultiAlternatives(subject, body, from_email, [to_email])
        if html_email_template_name:
            html_email = loader.render_to_string(html_email_template_name, context)
            email_message.attach_alternative(html_email, "text/html")

        try:
            email_message.send()
        except Exception:
            logger.exception("Failed to send password reset email to %s", context["user"].pk)

    def get_users(self, email):
        """
        Given an email, return matching user(s) who should receive a reset email.
        """
        email_field_name = UserModel.get_email_field_name()
        active_users = UserModel._default_manager.filter(
            **{f"{email_field_name}__iexact": email, "is_active": True}
        )

        return (
            u
            for u in active_users
            if u.has_usable_password() and u.email.lower() == email.lower()
        )

    def save(
        self,
        domain_override=None,
        subject_template_name="registration/password_reset_subject.txt",
        email_template_name="registration/password_reset_email.html",
        use_https=False,
        token_generator=default_token_generator,
        from_email=None,
        request=None,
        html_email_template_name=None,
        extra_email_context=None,
    ):
        """
        Generate a one-use password reset link and send it to the user.
        """
        email = self.cleaned_data["email"]
        if not domain_override:
            current_site = get_current_site(request)
            site_name = current_site.name
            domain = current_site.domain
        else:
            site_name = domain = domain_override

        # Get users matching the provided email
        users = list(self.get_users(email))  # Convert the generator to a list to evaluate if any user exists

        if not users:
            # If no users are found, display a warning message using Django's messages framework.
            messages.warning(request, "No user found with that email address.")
            return  # Return without proceeding with sending emails
        
        # Send the password reset email for each user
        for user in users:
            user_email = user.email
            context = {
                "email": user_email,
                "domain": domain,
                "site_name": site_name,
                "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                "user": user,
                "token": token_generator.make_token(user),
                "protocol": "https" if use_https else "http",
                **(extra_email_context or {}),
            }
            self.send_mail(
                subject_template_name,
                email_template_name,
                context,
                from_email,
                user_email,
                html_email_template_name=html_email_template_name,
            )

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.',widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Email Address'}),required=True)
    first_name = forms.CharField(max_length=30, required=True, help_text='Required.',widget=forms.TextInput(attrs={'class':'form-control','placeholder':'First Name'}))
    last_name = forms.CharField(max_length=30, required=False, help_text='Required',widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Second Name'}))
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox)
    class Meta:
        model = User
        fields = ['username','first_name','last_name','email','password1','password2']

    def __init__(self, *args,**kwargs):
        super(SignUpForm,self).__init__(*args,**kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'Username'
        self.fields['username'].label = ''
        self.fields['username'].help_text = '<span class="text-muted">Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</span>'

        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password1'].label = ''
        self.fields['password1'].help_text = '<ul class="form-text text-muted small"><li>Your password can’t be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can’t be a commonly used password.</li><li>Your password can’t be entirely numeric.</li></ul>'

        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
        self.fields['password2'].label = ''
        self.fields['password2'].help_text = '<span class="form-text text-muted">Enter the same password as before, for verification.</span>' 


# UserModel = get_user_model()

class LoginForm(forms.Form):
    """
    Custom form for authenticating users using their email and password.
    """
    email = forms.EmailField(
        label=_("Email"),
        widget=forms.EmailInput(attrs={"autofocus": True, "class": "form-control"}),
    )
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "current-password", "class": "form-control"}),
    )
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox)

    error_messages = {
        "invalid_login": _(
            "Please enter a correct email and password. Note that both "
            "fields may be case-sensitive."
        ),
        "inactive": _("This account is inactive."),
    }

    def __init__(self, request=None, *args, **kwargs):
        """
        Initialize the form, setting up the request parameter for custom authentication use.
        """
        self.request = request
        self.user_cache = None
        super().__init__(*args, **kwargs)

    def clean(self):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")

        if email and password:
            self.user_cache = authenticate(self.request, email=email, password=password)
            if self.user_cache is None:
                raise self.get_invalid_login_error()
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data

    def confirm_login_allowed(self, user):
        """
        Controls whether the given User may log in. This checks if the user is active.
        """
        if not user.is_active:
            raise ValidationError(
                self.error_messages["inactive"],
                code="inactive",
            )

    def get_user(self):
        """
        Returns the authenticated user.
        """
        return self.user_cache

    def get_invalid_login_error(self):
        """
        Returns the error message for invalid login.
        """
        return ValidationError(
            self.error_messages["invalid_login"],
            code="invalid_login",
            params={"username": "email"},
        )



class EmailBackend(ModelBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(email__iexact=email)
            if user.check_password(password):
                return user
        except UserModel.DoesNotExist:
            return None



