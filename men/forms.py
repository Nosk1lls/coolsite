from django import forms
from .models import Men
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .mixins import FormControlMixin


class AddPostForm(FormControlMixin, forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["cat_id"].empty_label = "Категория не выбрана"

    class Meta:
        model = Men
        fields = ["title", "slug", "content", "photo", "is_published", "cat_id"]


class RegisterUserForm(FormControlMixin, UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")


class ContactForm(FormControlMixin, forms.Form):
    name = forms.CharField(label="Имя", max_length=100)
    email = forms.EmailField(label="Email")
    content = forms.CharField(label="Сообщение", widget=forms.Textarea)


class CustomLoginForm(FormControlMixin, AuthenticationForm):
    pass
