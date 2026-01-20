from django.urls import path
from . import views

app_name='site_admin'
urlpatterns = [
        path('', views.login, name="login"),
        path('login', views.login, name="login"),
        path('dashboard', views.dashboard, name="dashboard"),

        path('list-screen', views.list_screen, name="list_screen"),
        path('add-screen', views.add_screen, name="add_screen"),
        path('view-screen/<int:id>', views.view_screen, name="view_screen"),

        path('list-movie', views.list_movie, name='list_movie'),
        path('list-movie/<str:query>', views.list_movie, name='list_movie'),
        path('view-movie/<int:id>', views.view_movie, name='view_movie'),
        path('list-people', views.list_people, name='list_people'),
        path('list-people/<str:query>', views.list_people, name='list_people'),
        path('view-people/<int:id>', views.view_people, name='view_people'),
        path('list-user', views.list_user, name='list_user'),
        path('list-pro', views.list_pro, name='list_pro'),
        path('change-pro-status/<int:id>/<str:status>', views.change_pro_status, name='change_pro_status'),
        path('search-movie', views.search_movie, name='search_movie'),
        path('logout', views.logout, name='logout'),
]
