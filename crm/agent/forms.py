from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from userprofile.models import CustomUser


User = get_user_model()

class AgentModelForm(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            'username',   
        )


class AddAgentForm(forms.Form):
    def __init__(self, organization, *args, **kwargs):
        super(AddAgentForm, self).__init__(*args, **kwargs)
        self.fields['agent'].queryset = CustomUser.objects.filter(is_agent=True).exclude(organizations=organization)
    agent = forms.ModelChoiceField(
        queryset=CustomUser.objects.none(), label='Select Agent')
