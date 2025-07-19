from django.contrib.auth.views import LoginView
from django.views.generic import ListView, DetailView, CreateView, TemplateView
from django.views.generic.edit import FormView
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import logout, login
from django.urls import reverse_lazy

from .models import Men, Category
from .forms import AddPostForm, RegisterUserForm, ContactForm, CustomLoginForm
from .utils import DataMixin


class MenHome(DataMixin, ListView):
    model = Men
    template_name = "men/index.html"
    context_object_name = "posts"

    def get_queryset(self):
        return Men.objects.filter(is_published=True).select_related("cat_id")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Главная страница")
        return {**context, **c_def}


class ShowPost(DataMixin, DetailView):
    model = Men
    template_name = "men/post.html"
    slug_url_kwarg = "post_slug"
    context_object_name = "post"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.object
        c_def = self.get_user_context(title=post.title, cat_selected=post.cat_id)
        return {**context, **c_def}


class MenCategory(DataMixin, ListView):
    model = Men
    template_name = "men/index.html"
    context_object_name = "posts"
    allow_empty = False

    def get_queryset(self):
        self.category = get_object_or_404(Category, slug=self.kwargs["cat_slug"])
        return Men.objects.filter(cat_id=self.category).select_related("cat_id")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(
            title=f"Рубрика: {self.category.name}", cat_selected=self.category.id
        )
        return {**context, **c_def}


class AddPage(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddPostForm
    template_name = "men/addpage.html"
    success_url = reverse_lazy("home")
    login_url = reverse_lazy("home")
    raise_exception = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Добавление статьи")
        return {**context, **c_def}


class AboutView(DataMixin, TemplateView):
    template_name = "men/about.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="О нас")
        return {**context, **c_def}


class ContactView(DataMixin, TemplateView):
    template_name = "men/contact.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Обратная связь")
        return {**context, **c_def}


class LoginView(DataMixin, LoginView):
    form_class = CustomLoginForm
    template_name = "men/login.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Авторизация")
        return {**context, **c_def}

    def get_success_url(self):
        return reverse_lazy("home")


class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = "men/register.html"
#    success_url = reverse_lazy("login")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Регистрация")
        return {**context, **c_def}

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect("home")


class ContactFormView(DataMixin, FormView):
    form_class = ContactForm
    template_name = "men/contact.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Обратная связь")
        return {**context, **c_def}

    def form_valid(self, form):
        print(form.cleaned_data)
        return redirect("home")


def logout_user(request):
    logout(request)
    return redirect("login")
