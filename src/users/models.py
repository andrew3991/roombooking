# vgl. https://www.youtube.com/watch?v=HshbjK1vDtY
# vgl. https://github.com/codingforentrepreneurs/eCommerce/tree/master/src
# vgl. https://studygyaan.com/django/how-to-signup-user-and-send-confirmation-email-in-django
# vgl. https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html
# vgl. https://www.youtube.com/watch?time_continue=103&v=gEbbso4XG00&feature=emb_logo

from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager
)
from django.core.mail import send_mail
from companies.models import Company
from django.conf import settings


class UserManager(BaseUserManager):
    def create_user(self,
                    email,
                    first_name,
                    last_name,
                    password=None,
                    is_active=True,
                    is_staff=False,
                    is_simpleuser=True,
                    is_advanceduser=False,
                    is_admin=False):
        if not email:
            raise ValueError('Users must have an email address')
        if not password:
            raise ValueError('Users must have a password')
        if not first_name:
            raise ValueError('Users must have a first name')
        if not last_name:
            raise ValueError('Users must have a last name')

        user_obj = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name
        )
        user_obj.set_password(password)
        user_obj.staff = is_staff
        user_obj.simpleuser = is_simpleuser
        user_obj.advanceduser = is_advanceduser
        user_obj.admin = is_admin
        user_obj.active = is_active
        user_obj.save(using=self._db)
        return user_obj

    def create_simpleuser(self, email, first_name, last_name, password=None):
        user = self.create_user(
            email,
            first_name,
            last_name,
            password=password,
            is_simpleuser=True
        )
        return user

    def create_advanceduser(self, email, first_name, last_name, password=None):
        user = self.create_user(
            email,
            first_name,
            last_name,
            password=password,
            is_simpleuser=True,
            is_advanceduser=True
        )
        return user

    def create_superuser(self,
                         email,
                         first_name,
                         last_name,
                         password=None):
        user = self.create_user(
            email,
            first_name,
            last_name,
            password=password,
            is_staff=True,
            is_simpleuser=True,
            is_advanceduser=True,
            is_admin=True
        )
        return user


class User(AbstractBaseUser):
    email = models.EmailField(max_length=255, unique=True)
    email_confirmed = models.BooleanField(default=False)
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    active = models.BooleanField(default=False)  # can login
    staff = models.BooleanField(default=False)  # staff user | non superuser
    simpleuser = models.BooleanField(default=True)
    advanceduser = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)  # superuser
    timestamp = models.DateTimeField(auto_now_add=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = UserManager()

    def __str__(self):
        # vgl. https://stackoverflow.com/questions/40618356/error-with-str-returned-non-string-type-int
        return '{}, {} '.format(self.email, self.last_name)

    def get_full_name(self):
        return self.last_name

    def get_short_name(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_simpleuser(self):
        return self.simpleuser

    @property
    def is_advanceduser(self):
        return self.advanceduser

    @property
    def is_admin(self):
        return self.admin

    @property
    def is_active(self):
        return self.active


class UpgradeRequest(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL,
                                 on_delete=models.CASCADE, related_name='receiver')
    message = models.CharField(max_length=255)
    in_progress = models.BooleanField(default=False)

    def __str__(self):
        return 'sender: {}, receiver: {} '.format(self.sender, self.receiver)
