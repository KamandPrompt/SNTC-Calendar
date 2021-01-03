from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.forms import ValidationError

class IITMandiAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        print("email : ",sociallogin.user.email)
        print(sociallogin.user, type(sociallogin.user))
        emailsplit = sociallogin.user.email.split('@')
        if len(emailsplit) <2:
            raise ValidationError('You are not authorized. Contact Admin.')
        else:    
            email_domain = emailsplit[1].lower()
            email_user = emailsplit.lower()
            if 'iitmandi.ac.in' not in email_domain or not email_user.isalpha():
                raise ValidationError(sociallogin.user.email + 'is not authorized to access Activities. Contact Admin.')
            else:
                pass

