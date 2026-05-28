from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.utils import timezone
from .models import PlayerScore, PlayerProfile
import json

def register_view(request):
    error = None
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password1 = request.POST.get('password1', '')
        password2 = request.POST.get('password2', '')
        nickname = request.POST.get('nickname', '').strip()

        if not username or not password1 or not nickname:
            error = "All fields are required."
        elif password1 != password2:
            error = "Passwords do not match."
        elif len(password1) < 6:
            error = "Password must be at least 6 characters."
        elif User.objects.filter(username=username).exists():
            error = "Username already taken."
        else:
            user = User.objects.create_user(username=username, password=password1)
            PlayerProfile.objects.create(user=user, nickname=nickname)
            login(request, user)
            return redirect('/')

    return render(request, 'bee/register.html', {'error': error})

@login_required
def game_view(request):
    nickname = request.user.username
    try:
        nickname = request.user.playerprofile.nickname
    except PlayerProfile.DoesNotExist:
        pass
    return render(request, 'bee/play.html', {'player_name': nickname})

@login_required
def leaderboard_view(request):
    from collections import OrderedDict
    panels = OrderedDict()
    for key in ('easy', 'medium', 'hard'):
        panels[key] = list(PlayerScore.objects.filter(difficulty=key).order_by('-score')[:10])
    return render(request, 'bee/leaderboard.html', {'panels': panels})

@login_required
def my_scores_view(request):
    nickname = request.user.username
    try:
        nickname = request.user.playerprofile.nickname
    except PlayerProfile.DoesNotExist:
        pass
    diffs = []
    for key, label in [('easy', 'Easy'), ('medium', 'Medium'), ('hard', 'Hard')]:
        entry = PlayerScore.objects.filter(name=nickname, difficulty=key).first()
        diffs.append({'key': key, 'label': label, 'entry': entry})
    return render(request, 'bee/my_scores.html', {
        'diffs': diffs, 'player_name': nickname,
    })

@csrf_exempt
def save_score(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            name = data.get('name', 'Anonymous')
            new_score = data.get('score', 0)
            difficulty = data.get('difficulty', 'easy')

            existing = PlayerScore.objects.filter(name=name, difficulty=difficulty).first()
            if existing:
                if new_score > existing.score:
                    existing.score = new_score
                    existing.date_achieved = timezone.now()
                    existing.save()
            else:
                PlayerScore.objects.create(name=name, score=new_score, difficulty=difficulty)

            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error'}, status=405)