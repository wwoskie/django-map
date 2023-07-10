from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('authors/', views.AuthorListView.as_view(), name='authors'),
    path('author/<int:pk>', views.AuthorDetailView.as_view(), name='author-detail'),
]

urlpatterns += [
    path('mygraphs/', views.UserCreatedGraphListView.as_view(), name='my-graphs'),
]

urlpatterns += [
    path('map/', views.map, name='map'),
]