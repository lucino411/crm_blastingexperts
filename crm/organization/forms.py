from django import forms
from userprofile.models import CustomUser
from .models import Organization

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



