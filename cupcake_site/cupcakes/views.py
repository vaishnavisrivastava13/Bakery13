from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from .models import Cupcake

def cupcakes(request):
    cupcakes = Cupcake.objects.all()
    paginator = Paginator(cupcakes, 8)  # 8 cakes per page

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'cupcakes.html', {
        'cupcakes': page_obj,
        'active_menu': 'cupcakes'
    })

def cupcake_detail(request, id):
    cupcake = get_object_or_404(Cupcake, id=id)
    return render(request, 'cupcake_detail.html', {'cupcake': cupcake})