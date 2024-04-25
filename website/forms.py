from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Record
import pandas as pd

class VerificationForm(forms.Form):
    verification_id = forms.CharField(label="Verification ID", max_length=100, required=True,
                                      widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Verification ID'}))


class SignUpForm(UserCreationForm):
    email = forms.EmailField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Email Address'}))
    first_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'First Name'}))
    last_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Last Name'}))



    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')


    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'User Name'
        self.fields['username'].label = ''
        self.fields['username'].help_text = '<span class="form-text text-muted"><small>Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</small></span>'

        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password1'].label = ''
        self.fields['password1'].help_text = '<ul class="form-text text-muted small"><li>Your password can\'t be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can\'t be a commonly used password.</li><li>Your password can\'t be entirely numeric.</li></ul>'

        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
        self.fields['password2'].label = ''
        self.fields['password2'].help_text = '<span class="form-text text-muted"><small>Enter the same password as before, for verification.</small></span>'    

    def clean_verification_id(self):
        verification_id = self.cleaned_data.get('verification_id')
        # Check the verification ID here
        if verification_id != "HLSHRADMIN":
            raise forms.ValidationError('Invalid verification ID.')
        return verification_id


# Create Add Record Form
class AddRecordForm(forms.ModelForm):
    first_name = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"First Name", "class":"form-control"}), label="")
    last_name = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"Last Name", "class":"form-control"}), label="")
    email = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"Email", "class":"form-control"}), label="")
    phone = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"Phone", "class":"form-control"}), label="")
    platform = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"Platform", "class":"form-control"}), label="")
    country = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"Country", "class":"form-control"}), label="")
    language = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"Native language", "class":"form-control"}), label="")
    language1 = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"Language 1", "class":"form-control"}), label="")
    language2 = forms.CharField(required=False, widget=forms.widgets.TextInput(attrs={"placeholder":"Language 2", "class":"form-control"}), label="")
    language3 = forms.CharField(required=False, widget=forms.widgets.TextInput(attrs={"placeholder":"Language 3", "class":"form-control"}), label="")
    language4 = forms.CharField(required=False, widget=forms.widgets.TextInput(attrs={"placeholder":"Language 4", "class":"form-control"}), label="")
    language5 = forms.CharField(required=False, widget=forms.widgets.TextInput(attrs={"placeholder":"Language 5", "class":"form-control"}), label="")
    status = forms.ChoiceField
    rate_type = forms.ChoiceField
    specificrate = forms.IntegerField
    contract_type = forms.ChoiceField
    agent_type = forms.ChoiceField
    AGE_CHOICES = [(i, i) for i in range(18, 100)]  # i assume this is the allowed minumum age
    age = forms.IntegerField(widget=forms.Select(choices=AGE_CHOICES))
    gender = forms.ChoiceField
    startdateM = forms.ChoiceField
    startdateD = forms.ChoiceField
    startdateY = forms.ChoiceField
    note = forms.Textarea

    class Meta:
        model = Record
        exclude = ("user",)



class ExcelUploadForm(forms.Form):
    excel_file = forms.FileField(label="", widget=forms.FileInput(attrs={'class': 'form-control', 'placeholder': 'Select Excel File'}))

    def clean_excel_file(self):
        file = self.cleaned_data['excel_file']
        if file and file.name.lower().endswith('.xlsx'):
            return file
        else:
            raise forms.ValidationError('Invalid file type. Please upload an Excel file (.xlsx).')

    def save(self):
        df = pd.read_excel(self.cleaned_data['excel_file'], names=["first_name", "last_name", "email", "phone", "platform", "country", "language", "language1", "language2", "language3", "language4", "language5", "age", "gender", "startdate"])

        for index, row in df.iterrows():
            record = Record.objects.create(
                first_name=row.get('first_name', ''), #excel file row 1 (FIRST NAME)
                last_name=row.get('last_name', ''), #excel file row 2 (LAST NAME)
                email=row.get('email', ''), #excel file row 3 (EMAIL ADRESS)
                phone=row.get('phone', ''), #excel file row 4 (PHONE NUMBER)
                platform=row.get('platform', ''), #excel file row 5 (PLATFORM)
                country=row.get('country', ''), #excel file row 6 (COUNTRY OF RESIDENCE)
                language=row.get('language', ''), #excel file row 7 (NATIVE LANGUAGE)
                language1=row.get('language1', ''), #excel file row 8 (SECOND LANGYAGE)
                language2=row.get('language2', ''), #excel file row 9 (EXTRA LANGUAGE 1)
                language3=row.get('language3', ''), #excel file row 10 (EXTRA LANGUAGE 1)
                language4=row.get('language4', ''), #excel file row 11 (EXTRA LANGUAGE 1)
                language5=row.get('language5', ''), #excel file row 12 (EXTRA LANGUAGE 1)
                age=row.get('age', ''), #excel file row 13 (AGE)
                #gender=row.get('gender', ''), #excel file row 14 (GENDER)
                #startdate=row.get('startdate', ''), #excel file row 15 (STARTDATE)

            )
            record.save()

