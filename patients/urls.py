from django.urls import path

from patients import views

app_name = 'patients'
urlpatterns = [
    path('list/', views.card_list, name="card_list"),
    path('add/', views.add_card, name="add_card"),
    path('info/<int:card_id>/', views.card_info, name="card_info"),
    path('<int:card_id>/add_note/', views.add_note, name="add_note"),
    path('edit_note/<int:note_id>', views.edit_note, name="edit_note"),
    path('info/<int:card_id>/edit', views.edit_card_info, name="edit_card_info"),
    path('info/<int:card_id>/delete', views.card_delete, name="card_delete"),
    path('delete_note/<int:note_id>', views.delete_note, name="delete_note")
]