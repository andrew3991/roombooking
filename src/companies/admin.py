# vgl. https://www.youtube.com/watch?v=HshbjK1vDtY
# vgl. https://github.com/codingforentrepreneurs/eCommerce/tree/master/src

from django.contrib import admin
from .models import Company


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'pk')
