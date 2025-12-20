from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Gift

def gift_list(request):
    gift_list = Gift.objects.all()
    gift_count = gift_list.count()

    paginator = Paginator(gift_list, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'gift.html', {   # 👈 direct name
        'gifts': page_obj,
        'gift_count': gift_count,
        'active_menu': 'gift'
    })


def gift_detail(request, id):
    gift = get_object_or_404(Gift, id=id)
    return render(request, 'gift_detail.html', {   # 👈 direct name
        'gift': gift
    })
