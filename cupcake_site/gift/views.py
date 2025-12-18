from django.shortcuts import render

def gift(request):
    return render(request, 'gift.html', {'active_menu': 'gift'})

