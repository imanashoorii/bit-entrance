from django.urls import path
from .views import ArticleListView, RateArticleView

urlpatterns = [
    path('articles/', ArticleListView.as_view(), name='article-list'),
    path('articles/<int:article_id>/rate/', RateArticleView.as_view(), name='rate-article'),
]
