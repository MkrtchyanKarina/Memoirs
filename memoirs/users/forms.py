from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label="Логин", widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    class Meta:
        model = get_user_model()  # функция возвращает текущую модель пользователя
        fields = ['username', 'password']


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label="Логин", widget=forms.TextInput(attrs={'class': 'form-input'}))
    email = forms.EmailField(label="Почта", widget=forms.EmailInput(attrs={'class': 'form-input'}))
    first_name = forms.CharField(label="Имя", widget=forms.TextInput(attrs={'class': 'form-input'}))
    last_name = forms.CharField(label="Фамилия", widget=forms.TextInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(label="Пароль", widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label="Повтор пароля", widget=forms.PasswordInput(attrs={'class': 'form-input'}))


    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']


    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password1'] != cd['password2']:
            raise forms.ValidationError("Пароли не совпадают")
        return cd["password1"]

    def clean_email(self):
        email = self.cleaned_data['email']
        if get_user_model().objects.filter(email=email).exists():
            raise forms.ValidationError("Этот адрес уже занят")
        return email


class EditUserForm(UserChangeForm):
    password = None

    username = forms.CharField(label="Логин", widget=forms.TextInput(attrs={'class': 'form-input'}), help_text="Обязательное поле. Не более 150 символов.")
    email = forms.EmailField(label="Почта", widget=forms.EmailInput(attrs={'class': 'form-input'}), required=True)
    first_name = forms.CharField(label="Имя", widget=forms.TextInput(attrs={'class': 'form-input'}), required=False)
    last_name = forms.CharField(label="Фамилия", widget=forms.TextInput(attrs={'class': 'form-input'}), required=False)

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'first_name', 'last_name']

    def clean_email(self):
        current_email = self.instance.email
        new_email = self.cleaned_data['email']
        if new_email != current_email:
            if get_user_model().objects.filter(email=new_email).exists():
                raise forms.ValidationError("Этот адрес уже занят")
        return new_email

    def clean_username(self):
        username = self.cleaned_data['username']
        if len(username) > 150:
            raise forms.ValidationError('Логин слишком длинный')
        return username
