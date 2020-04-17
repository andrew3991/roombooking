# vgl. https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html#onetoone
# vgl. https://stackoverflow.com/questions/15308901/initializing-after-first-superuser-is-created
# vgl. https://docs.djangoproject.com/en/3.0/topics/db/examples/many_to_one/

from users.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from companies.models import Company

# As soon as an admin (superuser) is created, a company is automatically
# created with default values for name and domain
@receiver(post_save, sender=User)
def create_admin_company(sender, instance, created, **kwargs):
    if created:
        if instance.is_admin:
            company = Company.objects.create(created_by=instance)
            company.user_set.add(instance)
            company.save()
            instance.save()
