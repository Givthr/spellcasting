# urls.py
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from bee.views import game_view, game_arena_view, save_score, leaderboard_view, my_scores_view, register_view

# Custom view configurations to dynamically serve PWA system files with the correct HTTP Headers
class PWAJavaScriptView(TemplateView):
    content_type = 'application/javascript'

class PWAJsonView(TemplateView):
    content_type = 'application/json'

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # --- PWA CONFIGURATION ROOT ROUTES ---
    path('sw.js', PWAJavaScriptView.as_view(template_name="bee/sw.js"), name='sw.js'),
    path('manifest.json', PWAJsonView.as_view(template_name="bee/manifest.json"), name='manifest.json'),
    # -------------------------------------

    path('', game_view, name='play_game'),
    path('game-arena/', game_arena_view, name='game_arena'),
    path('leaderboard/', leaderboard_view, name='leaderboard'),
    path('my-scores/', my_scores_view, name='my_scores'),
    path('api/save-score/', save_score, name='save_score'),

    path('login/', auth_views.LoginView.as_view(
        template_name='bee/login.html'
    ), name='login'),

    path('logout/', auth_views.LogoutView.as_view(
        template_name='bee/logout.html'
    ), name='logout'),

    path('register/', register_view, name='register'),
]

# Serves media and static assets when testing locally or running via development engines
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
