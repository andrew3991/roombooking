from django.db import models
# from users.models import User
from django.conf import settings


# vgl. https://docs.djangoproject.com/en/2.2/topics/auth/customizing/#substituting-a-custom-user-model
# vgl. https://stackoverflow.com/questions/34003865/django-reverse-query-name-clash
class Company(models.Model):
    name = models.CharField(max_length=255, default='company')
    created_by = models.OneToOneField(settings.AUTH_USER_MODEL,
                                      on_delete=models.CASCADE,
                                      related_name='+')
    email_domain = models.CharField(max_length=255, default='@yourdomain.com')

    def __str__(self):
        # vgl. https://stackoverflow.com/questions/40618356/error-with-str-returned-non-string-type-int
        return '{}'.format(self.name)
