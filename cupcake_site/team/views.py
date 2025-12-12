from django.shortcuts import render

# Create your views here.
def team_page(request):
    return render(request, 'team.html')