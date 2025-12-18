from django.shortcuts import render

def cupcakes(request):
    return render(request, 'cupcakes.html', {'active_menu': 'cupcakes'})