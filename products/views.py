import os, random
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.conf import settings
from .models import Product

# Create your views here.
# products/views.py

def product_list(request):
    # 505 Test language
    # raise Exception("Trigger 500")
    
    q = request.GET.get('q', '')
    qs = Product.objects.all()
    if q:
        qs = qs.filter(name__icontains=q)
        error = None if qs.exists() else f'No products found matching "{q}".'
    else:
        error = None

    paginator = Paginator(qs.order_by('id'), 20)
    page = paginator.get_page(request.GET.get('page'))

    # 1) preview absolute path
    preview_dir = os.path.join(settings.BASE_DIR, 'static', 'images', 'preview')
    try:
        preview_files = os.listdir(preview_dir)
    except FileNotFoundError:
        preview_files = []

    # 2) Dynamically bind apreview_page attribute to each product instance
    for prod in page:
        prod.preview_image = random.choice(preview_files)  # file name

    return render(request, 'products/product_list.html', {
        'page': page,
        'q': q,
    })


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)

    # 1) detail absolute path
    detail_dir = os.path.join(settings.BASE_DIR, 'static', 'images', 'detail')
    try:
        detail_files = os.listdir(detail_dir)
    except FileNotFoundError:
        detail_files = []

    # 2) random pick 3 pictures in all which they differ from each other
    selected = random.sample(detail_files, min(3, len(detail_files)))

    return render(request, 'products/product_detail.html', {
        'product': product,
        'detail_images': selected,  # name list
    })
