from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from .models import Beverage

def beverages(request):
    beverage_list = Beverage.objects.all()
    paginator = Paginator(beverage_list, 8)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'beverages.html', {
        'beverages': page_obj,
        'active_menu': 'beverages'
    })

def beverage_detail(request, id):
    beverage = get_object_or_404(Beverage, id=id)
    return render(request, 'beverage_detail.html', {
        'beverage': beverage
    })
