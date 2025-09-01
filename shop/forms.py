from django import forms
from .models import Signup


class SignupForm(forms.ModelForm):
    class Meta:
        model = Signup
        fields = ['name', 'email', 'phone', 'otp']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control bg-primary text-white',
                'autocomplete': 'name',
                'placeholder': 'Your Name',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control bg-primary text-white',
                'autocomplete': 'email',
                'placeholder': 'Email ID',
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control bg-primary text-white',
                'autocomplete': 'tel',
                'placeholder': 'Phone Number',
            }),
            'otp': forms.TextInput(attrs={
                'class': 'form-control bg-primary text-white',
                'autocomplete': 'one-time-code',
                'placeholder': 'OTP',
            }),
        }


class LoginForm(forms.Form):
    email = forms.EmailField()
    otp = forms.CharField(max_length=10)



class ContactForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control bg-primary text-dark fw-bold rounded text-center',
            'placeholder': 'Enter your Name'
        })
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control bg-primary text-dark fw-bold rounded text-center',
            'placeholder': 'Enter Email ID'
        })
    )
    phone = forms.CharField(
        max_length=15,
        widget=forms.TextInput(attrs={
            'class': 'form-control bg-primary text-dark fw-bold rounded text-center',
            'placeholder': 'Enter your number'
        })
    )
    message = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control bg-primary text-dark fw-bold rounded text-center',
            'placeholder': 'Enter Message'
        })
    )


class BillingForm(forms.Form):
    name = forms.CharField(max_length=100)
    street_address = forms.CharField(max_length=100)
    town_city = forms.CharField(max_length=50)
    postal_code = forms.CharField(max_length=10)
    
    PAYMENT_CHOICES = [
        ('cod', 'Cash on Delivery'),
        ('upi', 'UPI'),
        ('debit', 'Debit Card'),
        ('credit', 'Credit Card'),
    ]
    payment_method = forms.ChoiceField(choices=PAYMENT_CHOICES, widget=forms.RadioSelect)




