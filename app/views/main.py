from app.models import Image
from django.shortcuts import render


def index(request):
    images = Image.objects.all()[:5]
    context = {'images': images}
    return render(request, 'app/index.html', context)


def stats(request):
    return render(request, 'app/stats.html', {})
