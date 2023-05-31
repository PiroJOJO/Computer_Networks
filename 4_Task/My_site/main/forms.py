from django.forms import ModelForm, TextInput
from .models import URL

class URLForm(ModelForm):
    class Meta:
        model = URL
        fields = ['url']
        widgets = {
            'url': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите ссылку'
            })
        }