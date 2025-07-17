from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404, HttpResponse
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


def index(request):
    posts = Men.objects.all()
    context = get_common_context(cat_selected=0)
    context.update(
        {
            "posts": posts,
            "title": "Главная страница",
        }
    )
    return render(request, "men/index.html", context=context)


def about(request):
    context = get_common_context()
    context.update(
        {
            "title": "О нас",
        }
    )
    return render(request, "men/about.html", context=context)


def addpage(request):
    if request.method == "POST":
        form = AddPostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("home")
    else:
        form = AddPostForm()
    context = get_common_context(cat_selected=0)
    context.update(
        {
            "form": form,
            "title": "Добавление статьи",
        }
    )
    return render(request, "men/addpage.html", context=context)


def contact(request):
    context = get_common_context()
    context.update(
        {
            "title": "Обратная связь",
        }
    )
    return render(
        request, "men/contact.html", context=context
    )  # Лучше создать шаблон contact.html


def login(request):
    context = get_common_context()
    context.update(
        {
            "title": "Авторизация",
        }
    )
    return render(
        request, "men/login.html", context=context
    )  # Лучше создать шаблон login.html


def show_post(request, post_slug):
    post = get_object_or_404(Men, slug=post_slug)
    context = get_common_context(cat_selected=post.cat_id)
    context.update(
        {
            "post": post,
            "title": post.title,
        }
    )
    return render(request, "men/post.html", context=context)


def show_category(request, cat_slug):
    category = get_object_or_404(Category, slug=cat_slug)
    posts = Men.objects.filter(cat_id=category)
    if not posts.exists():
        raise Http404()
    context = get_common_context(cat_selected=category.id)
    context.update(
        {
            "posts": posts,
            "title": f"Рубрика: {category.name}",
        }
    )
    return render(request, "men/index.html", context=context)
