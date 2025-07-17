from django.views.generic import ListView, DetailView, CreateView, TemplateView
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.http import Http404
from .models import Men, Category
from .forms import AddPostForm

menu = [
    {"title": "О сайте", "url_name": "about"},
    {"title": "Добавить статью", "url_name": "add_page"},
    {"title": "Обратная связь", "url_name": "contact"},
    {"title": "Войти", "url_name": "login"},
]

def get_common_context(cat_selected=0):
    return {
        "menu": menu,
        "cats": Category.objects.all(),
        "cat_selected": cat_selected,
    }

class MenHome(ListView):
    model = Men
    template_name = "men/index.html"
    context_object_name = "posts"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_common_context(cat_selected=0))
        context["title"] = "Главная страница"
        return context

class ShowPost(DetailView):
    model = Men
    template_name = "men/post.html"
    slug_url_kwarg = "post_slug"
    context_object_name = "post"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_common_context(cat_selected=self.object.cat_id))
        context["title"] = self.object.title
        return context

class MenCategory(ListView):
    model = Men
    template_name = "men/index.html"
    context_object_name = "posts"
    allow_empty = False

    def get_queryset(self):
        self.category = get_object_or_404(Category, slug=self.kwargs["cat_slug"])
        return Men.objects.filter(cat_id=self.category)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_common_context(cat_selected=self.category.id))
        context["title"] = f"Рубрика: {self.category.name}"
        return context

class AddPage(CreateView):
    form_class = AddPostForm
    template_name = "men/addpage.html"
    success_url = reverse_lazy("home")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_common_context(cat_selected=0))
        context["title"] = "Добавление статьи"
        return context

class AboutView(TemplateView):
    template_name = "men/about.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_common_context())
        context["title"] = "О нас"
        return context

class ContactView(TemplateView):
    template_name = "men/contact.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_common_context())
        context["title"] = "Обратная связь"
        return context

class LoginView(TemplateView):
    template_name = "men/login.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_common_context())
        context["title"] = "Авторизация"
        return context
