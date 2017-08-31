from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from core.models import Owner


class OwnerSignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username']

    def __init__(self, *args, **kwargs):
        super(OwnerSignupForm, self).__init__(*args, **kwargs)

        for field in ['username', 'password1', 'password2']:
            self.fields[field].help_text = None

    def save(self, commit=True):
        user = super(OwnerSignupForm, self).save()
        owner = Owner(user=user)
        owner.save()
        return owner
