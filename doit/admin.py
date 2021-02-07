from django.contrib import admin
from .models import Doit

class DoitAdmin(admin.ModelAdmin):
    readonly_fields = ('created',)


admin.site.register(Doit, DoitAdmin)