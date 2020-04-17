# vgl. https://www.youtube.com/watch?v=HshbjK1vDtY
# vgl. https://github.com/codingforentrepreneurs/eCommerce/tree/master/src
# vgl. https://studygyaan.com/django/how-to-signup-user-and-send-confirmation-email-in-django
# vgl. https://github.com/CoreyMSchafer/code_snippets/blob/master/Django_Blog/12-Password-Reset/django_project/django_project/urls.py


from django.urls import path
from companies.views import (
    CompanyUpdateView
)

urlpatterns = [
    # Update Company
    path('update/<int:pk>', CompanyUpdateView.as_view(), name='updatecompany'),
]
