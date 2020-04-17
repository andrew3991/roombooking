from django.shortcuts import redirect
from companies.models import Company
from django.views.generic.edit import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages


# vgl. https://stackoverflow.com/questions/17985452/how-do-i-use-updateview
class CompanyUpdateView(LoginRequiredMixin, UpdateView):
    login_url = '/users/login/'
    model = Company
    fields = ['name', 'email_domain']
    template_name_suffix = '_update_form'
    success_url = '/users/profile/'

    # The currently logged in admin is allowed to only edit his own company
    # vgl. https://stackoverflow.com/questions/48664895/django-updateview-get-the-current-object-being-edit-id/48665754
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object != self.request.user.company:
            print('not the same company')
            msg = 'Wrong company! You are only allowed to edit your company!'
            messages.error(self.request, msg)
            return redirect('profile')
        return super(CompanyUpdateView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        context['company'] = self.object
        return context

    # Only admins are allowed to update a company item and only if it's the
    # company item that was created by the currently logged in admin
    # vgl. https://www.pkimber.net/howto/django/views/class-based-perm.html
    # vgl. https://docs.djangoproject.com/en/2.2/ref/views/#the-403-http-forbidden-view
    # vgl. https://stackoverflow.com/questions/27824181/django-a-class-based-view-with-mixins-and-dispatch-method
    # vgl. https://stackoverflow.com/questions/32983133/is-authenticated-raises-typeerror-typeerror-bool-object-is-not-callable
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if not self.request.user.is_admin:
            msg = 'Permission denied! You don`t have the permission to update companies!'
            messages.error(self.request, msg)
            return redirect('profile')
        return super(CompanyUpdateView, self).dispatch(request, *args, **kwargs)
