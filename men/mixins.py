from .models import Category

base_menu = [
    {"title": "О сайте", "url_name": "about"},
    {"title": "Обратная связь", "url_name": "contact"},
]

add_page_item = {"title": "Добавить статью", "url_name": "add_page"}


class DataMixin:
    paginate_by = 3

    def get_user_context(self, **kwargs):
        context = {
            **kwargs,
            "cats": Category.objects.all(),
            "cat_selected": kwargs.get("cat_selected", 0),
        }

        user_menu = base_menu.copy()

        if self.request.user.is_authenticated:
            user_menu.insert(1, add_page_item)
            context["is_auth"] = True
        else:
            context["is_auth"] = False

        context["menu"] = user_menu

        return context


class FormControlMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            existing_classes = field.widget.attrs.get("class", "")
            field.widget.attrs["class"] = (existing_classes + " form-input").strip()
