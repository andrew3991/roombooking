# vgl. https://www.youtube.com/watch?v=HshbjK1vDtY
# vgl. https://github.com/codingforentrepreneurs/eCommerce/tree/master/src
# vgl. https://www.youtube.com/watch?time_continue=103&v=gEbbso4XG00&feature=emb_logo

from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from users.models import User, UpgradeRequest
from companies.models import Company


class UserAdminCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('first_name',
                  'last_name',
                  'email')

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Passwords do not match')
        return password2

    def save(self, commit=True):
        user = super(UserAdminCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class UserAdminChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('first_name',
                  'last_name',
                  'email',
                  'password',
                  'active',
                  'admin')

    def clean_password(self):
        return self.initial['password']


class LoginForm(forms.Form):
    email = forms.EmailField(label='Email')
    password = forms.CharField(widget=forms.PasswordInput)


class RegisterForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    # vgl. https://stackoverflow.com/questions/1336900/django-modelchoicefield-and-initial-value
    # vgl. https://docs.djangoproject.com/en/3.0/ref/models/querysets/
    company = forms.ModelChoiceField(
        queryset=Company.objects.all().exclude(name='company'), initial=0)

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'email',
        )

    # vgl. https://www.youtube.com/watch?time_continue=103&v=gEbbso4XG00&feature=emb_logo
    def clean_company(self):
        chosen_company = self.cleaned_data.get('company')
        email = self.cleaned_data.get('email')
        msg = 'Not a valid email. Please enter your company based email with the domain %s' % chosen_company.email_domain
        if chosen_company.email_domain not in email:
            raise forms.ValidationError(msg)
        return chosen_company

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Passwords do not match')
        return password2

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


# Form for sending an admin a request to upgrade the own simple user account
class UpgradeRequestForm(forms.ModelForm):
    receiver = forms.ModelChoiceField(
        queryset=User.objects.all(),
        initial=0
    )

    class Meta:
        model = UpgradeRequest
        fields = (
            'message',
        )

    def __init__(self, *args, **kwargs):
        # vgl. https://stackoverflow.com/questions/50997267/django-pass-value-from-view-to-non-model-form-using-kwargs
        # vgl. https://stackoverflow.com/questions/1202839/get-request-data-in-django-form
        self.sender = kwargs.pop('sender', None)
        # print('self.sender: ', self.sender)
        # print('self.sender.pk: ', self.sender.pk)

        super(UpgradeRequestForm, self).__init__(*args, **kwargs)
        # print(self.fields['receiver'])
        # print(self.fields['receiver'].queryset)

        # Modifying field for receiver:
        # Select only admins that belong to the same company as the
        # currently logged in user
        # vgl. https://github.com/asifpy/django-crudbuilder/issues/23
        self.fields['receiver'].queryset = User.objects.filter(
            admin=True,
            company=self.sender.company
        )

    def save(self, commit=True):
        upgrade_request = super(UpgradeRequestForm, self).save(commit=False)
        if commit:
            upgrade_request.save()
        return upgrade_request
