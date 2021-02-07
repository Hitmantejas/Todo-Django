from django.forms import ModelForm
from .models import Doit


class DoitForm(ModelForm):
    class Meta:
        model = Doit
        fields = ['title', 'memo','important']

"""
"""