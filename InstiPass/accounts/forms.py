from allauth.account.forms import SignupForm

class CustomSignUpForm(SignupForm):
    def save(self,request):
        user = super().save(request)

        if "/institution" in request.path:
            user.role = "institution_admin"
        elif '/student' in request.path:
            user.role = "student"

        user.save()
        return user    