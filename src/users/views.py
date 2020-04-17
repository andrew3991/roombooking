# vgl. https://www.youtube.com/watch?v=HshbjK1vDtY
# vgl. https://github.com/codingforentrepreneurs/eCommerce/tree/master/src
# vgl. https://studygyaan.com/django/how-to-signup-user-and-send-confirmation-email-in-django
# vgl. https://simpleisbetterthancomplex.com/tutorial/2018/01/29/how-to-implement-dependent-or-chained-dropdown-list-with-django.html

from django.views.generic import (
    FormView,
    View,
)
from .forms import RegisterForm, LoginForm, UpgradeRequestForm
from users.models import User, UpgradeRequest
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.utils.http import is_safe_url
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from users.tokens import account_activation_token
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required


# Profile page
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import TemplateView
from django.views.generic import ListView


def home_page(request):
    context = {
        'title': 'Hello World!',
        'content': 'Welcome to the homepage.',
    }
    if request.user.is_authenticated:
        context['premium_content'] = 'Logged In'
    return render(request, 'home_page.html', context)


# vgl. https://docs.djangoproject.com/en/2.2/topics/auth/default/#django.contrib.auth.mixins.LoginRequiredMixin
# vgl. https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Authentication
# vgl. https://docs.djangoproject.com/en/3.0/ref/class-based-views/generic-display/#django.views.generic.detail.DetailView
class ProfileView(LoginRequiredMixin, TemplateView):
    login_url = '/users/login/'
    model = User
    template_name = 'users/profile.html'

    # The currently logged in admin is supposed to change the
    # default data (name, email_domain) of his company
    # vgl. https://docs.djangoproject.com/en/2.2/topics/class-based-views/mixins/
    def get(self, request, *args, **kwargs):
        self.object = self.request.user
        if self.object.is_admin:
            if self.object.company.name == 'company':
                msg = 'Change the company`s default name to your company`s name!'
                messages.error(request, msg)
            if self.object.company.email_domain == '@yourdomain.com':
                msg = 'Change the company`s default email domain to your company`s email domain!'
                messages.error(request, msg)
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context


class LoginView(FormView):
    form_class = LoginForm
    template_name = 'users/login.html'

    def form_valid(self, form):
        request = self.request
        next_ = request.GET.get('next')
        next_post = request.POST.get('next')
        redirect_path = next_ or next_post or None

        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            if is_safe_url(redirect_path, request.get_host()):
                return redirect(redirect_path)
            else:
                # vgl. https://realpython.com/django-redirects/
                return redirect('profile')
        return super(LoginView, self).form_invalid(form)


class RegisterView(View):
    form_class = RegisterForm
    template_name = 'users/register.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        # Get all the data input from the form
        form = self.form_class(request.POST)

        if form.is_valid():
            # Save the data input from the form to create a new user
            user = form.save(commit=False)

            # Get the entered company
            # vgl. https://docs.djangoproject.com/en/2.2/topics/forms/
            company = form.cleaned_data['company']
            print('company (view): ', company)

            user.save()

            # Add the currently saved user to the company object so that
            # the given company and the user are related to each other
            company.user_set.add(user)
            print('all company`s users: ', company.user_set.all())
            print('the users`s company: ', user.company)
            company.save()

            current_site = get_current_site(request)
            subject = 'Activate Your MySite Account'
            message = render_to_string('users/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)

            messages.success(request, ('Please confirm your email to complete registration.'))

            return redirect('login')

        return render(request, self.template_name, {'form': form})


class ActivateAccount(View):
    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            user.active = True
            user.email_confirmed = True
            user.save()
            login(request, user)
            messages.success(request, ('Your account have been confirmed.'))
            return redirect('profile')
        else:
            messages.warning(
                request, ('The confirmation link was invalid, possibly because it has already been used.'))
            return redirect('profile')


# Request to be sent to the admin to become an advanced user;
# Access should only be granted to users with a certain occupational status.
# To achieve this the admin has to check manually if the simple user has the
# professional position to get an advanced account. If this is the case the
# admin upgrades the account of simple user in admin panel manually.
class UpgradeRequestCreateView(LoginRequiredMixin, View):
    login_url = '/users/login/'
    form_class = UpgradeRequestForm
    template_name = 'users/upgrade_request_form.html'

    def get(self, request, *args, **kwargs):
        # vgl. https://stackoverflow.com/questions/50997267/django-pass-value-from-view-to-non-model-form-using-kwargs
        form = self.form_class(sender=request.user)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        # Get all the data input from the form
        # vgl. https://stackoverflow.com/questions/5119994/get-current-user-in-django-form
        form = self.form_class(request.POST, sender=request.user)

        if form.is_valid():
            # Save the data input from the form to create a new user
            upgrade_request = form.save(commit=False)

            # Get the relevant data from request and form
            sender = self.request.user
            receiver = form.cleaned_data['receiver']
            print('sender: ', sender, ', ', sender.company)
            print('receiver: ', receiver, ', ', receiver.company)

            # Add receiver and sender
            upgrade_request.sender = sender
            upgrade_request.receiver = receiver
            print('upgrade_request: ', upgrade_request.sender.company,
                  ', ', upgrade_request.sender.email)

            # Save the request
            upgrade_request.save()

            msg = 'Your request has been sent!'
            messages.success(request, msg)

            return redirect('profile')
        return render(request, self.template_name, {'form': form})


# vgl. ProfileView
class RequestListView(LoginRequiredMixin, ListView):
    login_url = '/users/login/'
    template_name = 'users/requests_list.html'
    context_object_name = 'requests'

    # vgl. https://stackoverflow.com/questions/48664895/django-updateview-get-the-current-object-being-edit-id/48665754
    def get(self, request, *args, **kwargs):
        # Only admins get access to requests
        if not self.request.user.is_admin:
            print('no admin')
            msg = 'You are not an admin! Only admins receive requests.'
            messages.error(self.request, msg)
            return redirect('profile')

        # The currently logged in admin is allowed to only see
        # requests sent to him
        if self.kwargs['pk'] != self.request.user.pk:
            print('not the currently logged in user')
            msg = 'Wrong user id! You are only allowed to see requests sent to you!'
            messages.error(self.request, msg)
            return redirect('profile')
        return super(RequestListView, self).get(request, *args, **kwargs)

    # vgl. https://docs.djangoproject.com/en/3.0/topics/class-based-views/generic-display/
    def get_queryset(self):
        self.user = get_object_or_404(User, pk=self.kwargs['pk'])
        return UpgradeRequest.objects.filter(receiver=self.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.user
        return context


@login_required(login_url='/users/login/')
def upgrade_account(request, pk):
    if(request.user.is_admin):
        # user: sender of request
        # => Simple user who has sent the currently logged in
        # admin a request to upgrade the simple user account
        # vgl. https://docs.djangoproject.com/en/3.0/topics/http/shortcuts/
        user = get_object_or_404(User, pk=pk)
        upgrade_request = get_object_or_404(UpgradeRequest, sender=user)

        # Upgrade the account
        user.advanceduser = True
        user.save()

        # Note that the request has been processed
        if(user.is_advanceduser):
            upgrade_request.in_progress = True
        upgrade_request.save()

        # vgl. https://stackoverflow.com/questions/12615290/django-python-variables-inside-strings
        msg = 'The account of simple user {} is upgraded now!'.format(user)
        messages.success(request, msg)
    else:
        msg = 'You are not an admin!'
        messages.error(request, msg)
        redirect('profile')
    return redirect('profile')
