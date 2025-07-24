# utils.py или views.py

from .models import Category

menu = [
    {"title": "О сайте", "url_name": "about"},
    {"title": "Добавить статью", "url_name": "add_page"},
    {"title": "Обратная связь", "url_name": "contact"},
]


class DataMixin:
    paginate_by = 3

    def get_user_context(self, **kwargs):
        context = kwargs
        cats = Category.objects.all()

        user_menu = menu.copy()
        if not self.request.user.is_authenticated:
            user_menu.pop(1)

        context["menu"] = user_menu

        context["cats"] = cats
        if "cat_selected" not in context:
            context["cat_selected"] = 0
        return context


class FormControlMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            existing_classes = field.widget.attrs.get("class", "")
            field.widget.attrs["class"] = (existing_classes + " form-input").strip()
