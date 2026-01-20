from django.urls import path
from . import views

app_name='film_user'
urlpatterns = [
    path('login', views.login, name='login'),
    path('signup', views.signup, name="signup"),
    path('logout', views.logout, name='logout'),
    path('dashboard', views.dashboard, name="dashboard"),
    path('edit-profile', views.edit_profile, name='edit_profile'),
    path('edit-password', views.edit_password, name='edit_password'),
    path('edit-avatar', views.edit_avatar, name='edit_avatar'),
    path('list-movie', views.list_movie, name='list_movie'),
    path('list-movie/<str:query>', views.list_movie, name='list_movie'),
    path('view-movie/<int:id>', views.view_movie, name='view_movie'),
    path('list-people', views.list_people, name='list_people'),
    path('list-people/<str:query>', views.list_people, name='list_people'),
    path('view-people/<int:id>', views.view_people, name='view_people'),
    path('search-movie', views.search_movie, name='search_movie'),
    path('write-review', views.view_movie_write_review, name='view_movie_write_review'),
    path('buy-ticket/<int:id>', views.view_movie_buy_ticket, name='view_movie_buy_ticket'),
]
