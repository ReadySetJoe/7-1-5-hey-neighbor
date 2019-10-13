from django.urls import path

from . import views

app_name = 'tools'

urlpatterns = [
    path('<int:pk>/delete/', views.delete_view, name='delete'),
    path('new/', views.CreateView.as_view(), name='new'),
    path('<int:pk>/', views.increment_watchers, name='increment_watcher'),
    path('<str:selection>/', views.IndexView.as_view(), name='selection'),
    path('', views.IndexView.as_view(), name='index'),
]
