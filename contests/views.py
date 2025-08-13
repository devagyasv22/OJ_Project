from django.shortcuts import render
from django.utils import timezone
from .models import Contest

def contest_list(request):
    now = timezone.now()
    active_contests = Contest.objects.filter(start_time__lte=now, end_time__gte=now)
    upcoming_contests = Contest.objects.filter(start_time__gt=now)
    past_contests = Contest.objects.filter(end_time__lt=now)

    return render(request, 'contest.html', {
        'active_contests': active_contests,
        'upcoming_contests': upcoming_contests,
        'past_contests': past_contests,
    })
