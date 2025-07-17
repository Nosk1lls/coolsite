from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.urls import path

from .views import (
    MenHome, AboutView, AddPage, ContactView, LoginView,
    ShowPost, MenCategory
)

urlpatterns = [
    path("", MenHome.as_view(), name="home"),
    path("about/", AboutView.as_view(), name="about"),
    path("addpage/", AddPage.as_view(), name="add_page"),
    path("contact/", ContactView.as_view(), name="contact"),
    path("login/", LoginView.as_view(), name="login"),
    path("post/<slug:post_slug>/", ShowPost.as_view(), name="post"),
    path("category/<slug:cat_slug>/", MenCategory.as_view(), name="category"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
