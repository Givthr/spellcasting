from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from bee.views import game_view, save_score, leaderboard_view, my_scores_view, register_view

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', game_view, name='play_game'),

    path('game-arena/', game_arena_view, name='game_arena'),

    path('leaderboard/', leaderboard_view, name='leaderboard'),
    path('my-scores/', my_scores_view, name='my_scores'),

    path('api/save-score/', save_score, name='save_score'),

    path('login/', auth_views.LoginView.as_view(
        template_name='bee/login.html'
    ), name='login'),

    path('logout/', auth_views.LogoutView.as_view(
        next_page='/login/'
    ), name='logout'),

    path('register/', register_view, name='register'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
