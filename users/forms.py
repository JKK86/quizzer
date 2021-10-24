import django.forms as forms
from django.contrib.auth import get_user_model

User = get_user_model()


class RegistrationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

    username = forms.CharField(label="Użytkownik", max_length=32)
    password = forms.CharField(label="Hasło", min_length=8, widget=forms.PasswordInput)
    password_repeat = forms.CharField(label="Powtórz hasło", min_length=8, widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data['password']
        password_repeat = cleaned_data['password_repeat']
        if password and password_repeat and password != password_repeat:
            raise forms.ValidationError('Hasła nie są takie same')