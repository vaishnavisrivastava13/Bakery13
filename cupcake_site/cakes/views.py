from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from .models import Cake

def cake_list(request):
    cakes = Cake.objects.all()
    paginator = Paginator(cakes, 8)  # 8 cakes per page

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'cakes.html', {
        'cakes': page_obj,
        'active_menu': 'cakes'
    })

def cake_detail(request, id):
    cake = get_object_or_404(Cake, id=id)
    return render(request, 'cake_detail.html', {'cake': cake})