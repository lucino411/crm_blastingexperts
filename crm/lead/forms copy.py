from django import forms
from .models import Lead
from choices.choices import SALUTATION_CHOICES, LEGAL_NATURE_CHOICES, LEAD_SOURCE_CHOICES, LEAD_STATUS_CHOICES, LAST_CONTACTED_VIA_CHOICES
from option.models import Title, Currency, ProductCategory, Provider, Country
from userprofile.models import CustomUser

class AddLeadFormForRegistered(forms.ModelForm):
    salutation = forms.ChoiceField(choices=SALUTATION_CHOICES, widget=forms.Select(attrs={'class': 'form-select'}))
    first_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}))
    last_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}))
    primary_email = forms.EmailField(label="", widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
    phone = forms.CharField(label="", max_length=20, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone'}))
    company = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Company'}))
    title = forms.ModelChoiceField(queryset=Title.objects.all(), widget=forms.Select(attrs={'class': 'form-select'}))
    website = forms.URLField(label="", widget=forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Company Website'}))
    legal_nature = forms.ChoiceField(choices=LEGAL_NATURE_CHOICES, widget=forms.Select(attrs={'class': 'form-select'}))
    lead_source = forms.ChoiceField(choices=LEAD_SOURCE_CHOICES, widget=forms.Select(attrs={'class': 'form-select'}))
    lead_status = forms.ChoiceField(choices=LEAD_STATUS_CHOICES, widget=forms.Select(attrs={'class': 'form-select'}))
    last_contacted_via = forms.ChoiceField(choices=LAST_CONTACTED_VIA_CHOICES, widget=forms.Select(attrs={'class': 'form-select'}))
    currency = forms.ModelChoiceField(queryset=Currency.objects.all(), widget=forms.Select(attrs={'class': 'form-select'}))
    record_conversion_rate = forms.FloatField(required=False, widget=forms.NumberInput(attrs={'class': 'form-control'}))
    country = forms.ModelChoiceField(queryset=Country.objects.all(), widget=forms.Select(attrs={'class': 'form-select'}))
    city = forms.CharField(label="", max_length=100, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City'}))
    state = forms.CharField(label="", max_length=100, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'State'}))
    address = forms.CharField(label="", max_length=255, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Address'}))
    zip_code = forms.CharField(label="", max_length=20, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Zip Code'}))
    postal_code = forms.CharField(label="", max_length=20, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Postal Code'}))
    product_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Product Name'}))
    product_category = forms.ModelChoiceField(queryset=ProductCategory.objects.all(), widget=forms.Select(attrs={'class': 'form-select'}))
    product_website = forms.URLField(label="", widget=forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Product Website'}))
    provider = forms.ModelChoiceField(queryset=Provider.objects.all(), widget=forms.Select(attrs={'class': 'form-select'}))
    assigned_to = forms.ModelChoiceField(queryset=CustomUser.objects.all(), empty_label=None, widget=forms.Select(attrs={'class': 'form-select'}))


    def __init__(self, *args, **kwargs):
        super(AddLeadFormForRegistered, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['class'] = 'form-control'
        self.fields['first_name'].widget.attrs['placeholder'] = 'First Name'

        self.fields['last_name'].widget.attrs['class'] = 'form-control'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Last Name'

    def as_row(self):
        return self._html_output(
            normal_row='<div class="row">'
                       '<div class="col">'
                       '%(label)s %(field)s'
                       '</div>'
                       '</div>',
            error_row='%s',
            row_ender='</div>',
            help_text_html='',
            errors_on_separate_row=True,
        )

    class Meta:
        model = Lead
        fields = ('salutation', 'first_name', 'last_name', 'primary_email', 'phone', 'company', 'legal_nature', 'website', 'country', 'city', 'state', 'address', 'zip_code', 'postal_code', 'lead_source', 'lead_status', 'last_contacted_on', 'last_contacted_via', 'product_name', 'product_website', 'description', 'currency', 'record_conversion_rate', 
                  'product_category', 'provider', 'title', 'assigned_to')
        widgets = {
            'last_contacted_on': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'last_contacted_on': forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'format': '%Y-%m-%d'})
        }

class AddLeadFormForUnregistered(forms.ModelForm):
    salutation = forms.ChoiceField(choices=SALUTATION_CHOICES, widget=forms.Select(attrs={'class': 'form-select'}))
    first_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}))
    last_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}))
    primary_email = forms.EmailField(label="", widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
    phone = forms.CharField(label="", max_length=20, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone'}))
    title = forms.ModelChoiceField(queryset=Title.objects.all(), widget=forms.Select(attrs={'class': 'form-select'}))
    legal_nature = forms.ChoiceField(choices=LEGAL_NATURE_CHOICES, widget=forms.Select(attrs={'class': 'form-select'}))
    lead_source = forms.ChoiceField(choices=LEAD_SOURCE_CHOICES, widget=forms.Select(attrs={'class': 'form-select'}))
    lead_status = forms.ChoiceField(choices=LEAD_STATUS_CHOICES, widget=forms.Select(attrs={'class': 'form-select'}))
    last_contacted_via = forms.ChoiceField(choices=LAST_CONTACTED_VIA_CHOICES, widget=forms.Select(attrs={'class': 'form-select'}))
    currency = forms.ModelChoiceField(queryset=Currency.objects.all(), widget=forms.Select(attrs={'class': 'form-select'}))
    record_conversion_rate = forms.FloatField(required=False, widget=forms.NumberInput(attrs={'class': 'form-control'}))
    country = forms.ModelChoiceField(queryset=Country.objects.all(), widget=forms.Select(attrs={'class': 'form-select'}))
    city = forms.CharField(label="", max_length=100, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City'}))
    state = forms.CharField(label="", max_length=100, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'State'}))
    address = forms.CharField(label="", max_length=255, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Address'}))
    zip_code = forms.CharField(label="", max_length=20, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Zip Code'}))
    postal_code = forms.CharField(label="", max_length=20, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Postal Code'}))
    product_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Product Name'}))
    product_category = forms.ModelChoiceField(queryset=ProductCategory.objects.all(), widget=forms.Select(attrs={'class': 'form-select'}))
    product_website = forms.URLField(label="", widget=forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Product Website'}))
    provider = forms.ModelChoiceField(queryset=Provider.objects.all(), widget=forms.Select(attrs={'class': 'form-select'}))
    assigned_to = forms.ModelChoiceField(queryset=CustomUser.objects.all(), empty_label=None, widget=forms.Select(attrs={'class': 'form-select'}))

    def __init__(self, *args, **kwargs):
        super(AddLeadFormForUnregistered, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['class'] = 'form-control'
        self.fields['first_name'].widget.attrs['placeholder'] = 'First Name'
        self.fields['last_name'].widget.attrs['class'] = 'form-control'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Last Name'
        # self.fields['last_contacted_on'].widget = forms.DateTimeInput(format='%Y-%m-%d %H:%M:%S', attrs={
        #     'class': 'form-control',
        #     'type': 'datetime-local'
        # })

    def as_row(self):
        return self._html_output(
            normal_row='<div class="row">'
                       '<div class="col">'
                       '%(label)s %(field)s'
                       '</div>'
                       '</div>',
            error_row='%s',
            row_ender='</div>',
            help_text_html='',
            errors_on_separate_row=True,
        )
    
    class Meta:
        model = Lead
        fields = ('salutation', 'first_name', 'last_name', 'primary_email', 'phone', 'legal_nature', 'country', 'city', 'state', 'address', 'zip_code', 'postal_code', 'lead_source', 'lead_status', 'last_contacted_on', 'last_contacted_via', 'product_name', 'product_website', 'description', 'currency', 'record_conversion_rate', 
                  'product_category', 'provider', 'title', 'assigned_to')
        widgets = {
            # 'last_contacted_on': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),            
        }

