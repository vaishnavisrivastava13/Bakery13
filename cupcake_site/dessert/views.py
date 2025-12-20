from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from .models import Dessert

def dessert(request):
    dessert_list = Dessert.objects.all()
    paginator = Paginator(dessert_list, 8)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'dessert.html', {
        'desserts': page_obj,   # ✅ FIXED (plural)
        'active_menu': 'dessert'
    })

def dessert_detail(request, id):
    dessert = get_object_or_404(Dessert, id=id)
    return render(request, 'dessert_detail.html', {
        'dessert': dessert
    })
