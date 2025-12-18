from django.shortcuts import render

def desert(request):
    return render(request, 'desert.html', {'active_menu': 'desert'})

