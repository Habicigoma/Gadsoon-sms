from django.urls import path
from . import views

urlpatterns=[
    path('add_item/', views.add_item, name='add_item'),
    path('update_item/<int:pk>/', views.update_item, name='update_item'),
    path('all_items/', views.all_items, name='all_items'),
    path('delete-item/<int:pk>/', views.delete_item, name='delete_item'),
    path('issue_item/', views.issue_item, name='issue_item'),
    path('issue_history/', views.issue_history, name='issue_history'),
    path('return_item/', views.return_item, name='return_item'),
    path('return_history/', views.return_history, name='return_history'),
    path('restock_item/', views.restock_item, name='restock_item'),
    path('restock_history/', views.restock_history, name='restock_history'),
    path('delete_item/<int:pk>/', views.delete_item, name='delete_item'),


]