from django.shortcuts import render

# Create your views here.
def beverages(request):
        return render(request,'beverages.html', {'active_menu': 'beverages'})