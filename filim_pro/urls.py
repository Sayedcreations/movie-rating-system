from django.urls import path
from . import views

app_name='film_pro'
urlpatterns = [
    path('login', views.login, name='login'),
    path('signup', views.signup, name="signup"),
    path('logout', views.logout, name='logout'),
    path('dashboard', views.dashboard, name="dashboard"),
    path('edit-profile', views.edit_profile, name='edit_profile'),
    path('edit-password', views.edit_password, name='edit_password'),
    path('edit-avatar', views.edit_avatar, name='edit_avatar'),
    path('add-people', views.add_people, name='add_people'),
    path('list-people', views.list_people, name='list_people'),
    path('list-people/<str:query>', views.list_people, name='list_people'),
    path('view-people/<int:id>', views.view_people, name='view_people'),
    path('edit-people/<int:id>', views.edit_people, name='edit_people'),
    path('delete-people/<int:id>', views.delete_people, name='delete_people'),
    path('edit-people-avatar/<int:id>', views.edit_people_avatar, name='edit_people_avatar'),
    path('add-people-photo/<int:id>', views.add_people_photo, name='add_people_photo'),
    path('add-movie', views.add_movie, name='add_movie'),
    path('list-movie', views.list_movie, name='list_movie'),
    path('list-movie/<str:query>', views.list_movie, name='list_movie'),
    path('view-movie/<int:id>', views.view_movie, name='view_movie'),
    path('edit-movie/<int:id>', views.edit_movie, name='edit_movie'),
    path('edit-movie-avatar/<int:id>', views.edit_movie_avatar, name='edit_movie_avatar'),
    path('add-movie-photo/<int:id>', views.add_movie_photo, name='add_movie_photo'),
    path('edit-movie-cast/<int:id>', views.edit_movie_cast, name='edit_movie_cast'),
    path('edit-movie-crew/<int:id>', views.edit_movie_crew, name='edit_movie_crew'),
    path('delete-movie/<int:id>', views.delete_movie, name='delete_movie'),    
    path('search-movie', views.search_movie, name='search_movie'),
]
