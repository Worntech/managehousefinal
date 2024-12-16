from django.forms import ModelForm
from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm

class MyUserForm(UserCreationForm):
    class Meta:
        model = MyUser
        fields = ['first_name', 'last_name', 'email', 'username']


        
class ContactForm(ModelForm):
    class Meta:
        model = Contact
        fields = '__all__'


class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = ['Room_Name', 'Room_Number', 'Cost', 'Image']
        
# class MyPaymentForm(ModelForm):
#     class Meta:
#         model = MyPayment
#         fields = ['Month']
        
class MyPaymentForm(forms.Form):
    Month = forms.ChoiceField(
        choices=MyPayment.MONTH_CHOICES,  # Use MyPayment.MONTH_CHOICES
        widget=forms.Select(attrs={'class': 'form-control'})
    )
        
class PaymentForm(ModelForm):
    class Meta:
        model = Payment
        fields = []
