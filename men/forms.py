from django import forms
from .models import *


class AddPostForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["cat_id"].empty_label = "Категория не выбрана"

    class Meta:
        model = Men
        fields = ["title", "slug", "content", "photo", "is_published", "cat_id"]
        widgets = {
            "title": forms.TextInput(attrs={"size": 60}),
            "content": forms.Textarea(attrs={"cols": 60, "rows": 10}),
        }
