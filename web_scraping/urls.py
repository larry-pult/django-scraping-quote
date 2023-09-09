from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("quote/", views.quote, name="quote"),
    path("tag/", views.tag, name="tag"),
    path("author/", views.author, name="author"),
    path("quote/<int:quote_id>/", views.quote_by_quote_id, name="quote_by_quote_id"),
    path("tag/<int:tag_id>/", views.quote_by_tag_id, name="quote_by_tag_id"),
    path("author/<int:author_id>/", views.quote_by_author_id, name="quote_by_author_id"),
    path("run_scraping/", views.run_scraping, name="run_scraping")
]
