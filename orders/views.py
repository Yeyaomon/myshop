# orders/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Sum, F
import json, datetime

from products.models import Product
from .models import Order, OrderItem, Cart, CartItem


@login_required
def add_to_cart(request, product_id):
    """
    Add one unit of the product to the user’s cart and show cart.
    """
    cart, _ = Cart.objects.get_or_create(user=request.user)
    prod = get_object_or_404(Product, pk=product_id)
    item, _ = CartItem.objects.get_or_create(cart=cart, product=prod)
    item.quantity += 1
    item.save()
    return redirect('view_cart')


@login_required
def buy_product(request, product_id):
    """
    “Buy Now”: add specified quantity to cart then go directly to checkout.
    """
    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        qty = max(1, int(request.POST.get('quantity', 1)))
        if qty > product.stock:
            return render(request, 'orders/order_error.html', {'message': 'Out of stock'})
        cart, _ = Cart.objects.get_or_create(user=request.user)
        item, _ = CartItem.objects.get_or_create(cart=cart, product=product)
        item.quantity += qty
        item.save()
        return redirect('checkout')
    return redirect('product_detail', pk=product_id)


@login_required
def view_cart(request):
    """
    Render cart page; support edit/delete via GET param ?edit=1.
    """
    cart, _ = Cart.objects.get_or_create(user=request.user)
    edit_mode = request.GET.get('edit') == '1'
    return render(request, 'orders/cart.html', {
        'cart': cart,
        'edit_mode': edit_mode,
    })


@login_required
def checkout(request):
    """
    Checkout only selected items; others remain in cart.
    """
    cart = get_object_or_404(Cart, user=request.user)
    selected_ids = request.POST.getlist('item_ids')
    if not selected_ids:
        return render(request, 'orders/cart.html', {
            'cart': cart,
            'edit_mode': False,
            'error': 'Please select at least one item to checkout.'
        })

    order = Order.objects.create(user=request.user)
    for item in cart.items.filter(id__in=selected_ids):
        OrderItem.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity,
            price=item.product.price
        )
        item.product.stock -= item.quantity
        item.product.save()
        item.delete()

    total = order.orderitem_set.aggregate(
        total=Sum(F('quantity') * F('price'))
    )['total'] or 0
    order.total_amount = total
    order.save()
    return render(request, 'orders/checkout_success.html', {'order': order})


@login_required
def remove_from_cart(request):
    """
    Delete selected items from cart and return to normal view.
    """
    cart = get_object_or_404(Cart, user=request.user)
    selected_ids = request.POST.getlist('item_ids')
    for item in cart.items.filter(id__in=selected_ids):
        item.delete()
    return redirect('view_cart')


@login_required
def order_list(request):
    """
    Show past orders of the current user.
    """
    orders = Order.objects.filter(user=request.user).order_by('-order_date')
    return render(request, 'orders/order_list.html', {'orders': orders})


@login_required
def order_detail(request, order_id):
    """
    Show details of a single order.
    """
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'orders/order_detail.html', {'order': order})


@user_passes_test(lambda u: u.is_staff)
def admin_dashboard(request):
    """
    Admin Dashboard: show monthly order counts and top 5 products by revenue.
    """
    today = datetime.date.today()
    monthly = []
    for i in range(6):
        m = today.replace(day=1) - datetime.timedelta(days=30 * i)
        cnt = Order.objects.filter(
            order_date__year=m.year,
            order_date__month=m.month
        ).count()
        monthly.append((m.strftime('%Y-%m'), cnt))
    monthly_json = json.dumps(monthly)

    # Get top 5 products by revenue (Decimal sales)
    qs = (
        OrderItem.objects
        .values('product__name')
        .annotate(sales=Sum(F('quantity') * F('price')))
        .order_by('-sales')[:5]
    )
    # Convert Decimal to float for JSON serialization
    data = []
    for entry in qs:
        data.append({
            'product__name': entry['product__name'],
            'sales': float(entry['sales'] or 0),
        })
    cat_json = json.dumps(data)

    return render(request, 'orders/admin_dashboard.html', {
        'monthly_json': monthly_json,
        'cat_json':     cat_json,
    })
