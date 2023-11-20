from django import forms
from userprofile.models import CustomUser
from .models import Organization
from agent.models import Agent


class OrganizationModelForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = [            
            'is_organizator']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['is_organizator'].widget = forms.CheckboxSelectMultiple()
        self.fields['is_organizator'].queryset = CustomUser.objects.filter(
            is_organizator=True)


class OrganizationCreateModelForm(forms.ModelForm):
    class Meta:
        model = Organization
        fields = [            
            'name',
            'email',
            'created_by'
            ]
        

class AddAgentForm(forms.Form):
    def __init__(self, organization, *args, **kwargs):
        super(AddAgentForm, self).__init__(*args, **kwargs)
        # self.fields['agent'].queryset = CustomUser.objects.filter(is_agent=True).exclude(organizations=organization)
        self.fields['agent'].queryset = CustomUser.objects.filter(is_agent=True)
    agent = forms.ModelChoiceField(
        queryset=CustomUser.objects.none(), label='Select Agent')



