from django.forms import ModelForm
from .models import UserAppearance


class UserAppearanceForm(ModelForm):
    class Meta:
        model = UserAppearance
        labels = {
            "weight": "Your Weight (kg)",
            "height": "Your Height (cm)",
            "age": "Your age",
            "sex": "Choose sex",
        }
        fields = ['weight', 'height', 'age', 'sex']
