from django.contrib import admin

# Register your models here.
from roles.models import UserRoles

admin.site.register(UserRoles)
