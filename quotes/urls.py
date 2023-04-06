from django.urls import path
from . import views

app_name = 'quote'

urlpatterns = [
    path('', views.QuoteView.as_view(), name='index'),
    path('quotes/add/', views.QuoteView.as_view(), name='add-quote'),
    path('quotes/scrape/', views.QuoteView.as_view(), name='scrape-quotes'),
    path('quotes/edit/<int:pk>', views.QuoteUpdateView.as_view(), name='edit'),
    path('quotes/remove/<int:pk>', views.QuoteRemoveView.as_view(), name='remove'),
    path('tag/<str:tag>', views.QuoteView.as_view(), name='search-tag'),
    path('tag/add/', views.TagView.as_view(), name='add-tags'),
    path('author/<str:author>', views.AuthorView.as_view(), name='author'),
    path('author/add/', views.AuthorView.as_view(), name='add-author'),
    path('author/edit/<int:pk>', views.AuthorUpdateView.as_view(), name='edit-author'),
]