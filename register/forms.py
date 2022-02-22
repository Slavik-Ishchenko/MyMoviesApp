from django import forms
from django.conf import settings
from django.contrib.auth import get_user_model
User = get_user_model()


class SignInForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Имя пользователя'
        self.fields['password'].label = 'Пароль'
        self.fields['email'].label = 'Email-адрес'

    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        user = User.objects.filter(username=username).first()
        if not user:
            raise forms.ValidationError(f'Пользватель {username} не найден')
        if not user.check_password(password):
            raise forms.ValidationError('Пароль неверный')
        return self.cleaned_data

    class Meta:
        model = User
        fields = ['username', 'password', 'email']


class SignUpForm(forms.ModelForm):
    username = forms.CharField()
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput)
    date_of_birth = forms.DateField(input_formats=settings.DATE_INPUT_FORMATS)

    def __init__(self, *args, **kwargs):
        """Форма для заполнения данных при регистрации"""
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Имя пользователя'
        self.fields['email'].label = 'Email-адрес'
        self.fields['password'].label = 'Пароль'
        self.fields['password_confirm'].label = 'Подтвердите пароль'
        self.fields['date_of_birth'].label = 'Дата рождения (ДД.ММ.ГГГГ)'

    def clean_email(self):
        """Проверка уникальности Email-адреса"""
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(f'Почтовый адрес {email} уже зарегистрирован')
        return email

    def clean(self):
        """Проверка правильности ввода пароля"""
        password = self.cleaned_data['password']
        password2 = self.cleaned_data['password_confirm']
        if password != password2:
            raise forms.ValidationError(f'Пароли не совпадают')
        return self.cleaned_data

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password_confirm', 'date_of_birth']
