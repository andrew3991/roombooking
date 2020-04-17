# vgl. https://www.youtube.com/watch?v=HshbjK1vDtY
# vgl. https://github.com/codingforentrepreneurs/eCommerce/tree/master/src
# vgl. https://studygyaan.com/django/how-to-signup-user-and-send-confirmation-email-in-django
# vgl. https://github.com/CoreyMSchafer/code_snippets/blob/master/Django_Blog/12-Password-Reset/django_project/django_project/urls.py


from django.urls import path
from django.conf.urls import url
from users.views import (
    RegisterView,
    LoginView,
    ActivateAccount,
    ProfileView,
    UpgradeRequestCreateView,
    RequestListView,
)
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    # Registration | Login/Logout
    url(r'^register/$', RegisterView.as_view(), name='register'),
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^logout/$', LogoutView.as_view(template_name='users/logout.html'), name='logout'),

    # Profile
    path('profile/', ProfileView.as_view(), name='profile'),

    # Request to upgrade the simple user account
    path('request/upgrade/', UpgradeRequestCreateView.as_view(), name='request-upgrade'),

    # Show requests
    # vgl. https://stackoverflow.com/questions/56724551/unable-to-get-kwargs-from-get-queryset-of-listview
    path('<int:pk>/requests/', RequestListView.as_view(), name='requests'),

    # Upgrade account of simple user
    path('account/<int:pk>/upgrade/', views.upgrade_account, name='account-upgrade'),

    # Activation of User
    path('activate/<uidb64>/<token>/', ActivateAccount.as_view(), name='activate'),
]
