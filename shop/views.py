from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, ContactMessage, Cart, CartItem, Order, OrderItem
from django.db.models import Q
from .forms import ContactForm, LoginForm, BillingForm
from shop.forms import SignupForm
from django.contrib import messages
from .models import Signup

def home(request):
    return render(request, 'home.html')


def shop_view(request, category_name):
    category_title = None

    if category_name:
        category_title = category_name.replace('-', ' ').title()
        products = Product.objects.filter(category=category_name)
    else:
        products = Product.objects.all()

    price_filters = {
        '50-100': (50, 100),
        '100-200': (100, 200),
        '200-300': (200, 300),
        '300-500': (300, 500),
    }

    selected_filters = request.GET.getlist('price')

    if selected_filters:
        queries = Q()
        for f in selected_filters:
            if f in price_filters:
                low, high = price_filters[f]
                queries |= Q(price__gte=low, price__lte=high)
        products = products.filter(queries)

    # Define label/value pairs for template rendering
    price_ranges = [
        {'label': 'Rs. 50–100', 'value': '50-100'},
        {'label': 'Rs. 100–200', 'value': '100-200'},
        {'label': 'Rs. 200–300', 'value': '200-300'},
        {'label': 'Rs. 300–500', 'value': '300-500'},
    ]


    return render(request, 'shop.html', {
        'products': products,
        'price_ranges': price_ranges,
        'selected_filters': selected_filters,
        'category': category_title
    })


def product_description(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'productdescription.html', {
        'product': product,
        'features': product.feature_list(),
    })


def about_view(request):
    return render(request, 'about.html')


def contact_view(request):
    form = ContactForm()
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            ContactMessage.objects.create(**form.cleaned_data)
            messages.success(request, "Message sent and saved successfully!")
            return redirect('contact')
    return render(request, 'contact.html', {'form': form})


def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            print("Form valid: redirecting to login")
            form.save()
            return redirect('login')
        else:
            print("Form is INVALID")
            print(form.errors)  # Show detailed validation errors
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})




def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            otp = form.cleaned_data['otp']

            # Check if the email and OTP match an existing signup
            user = Signup.objects.filter(email=email, otp=otp).first()
            if user:
                # You can set session/cookie here
                return redirect('home')  # Or dashboard page
            else:
                form.add_error(None, "Invalid email or OTP.")
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})



def get_or_create_cart(request):
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        cart_id = request.session.get('cart_id')
        if cart_id:
            cart = Cart.objects.filter(id=cart_id).first()
            if cart:
                return cart
        cart = Cart.objects.create()
        request.session['cart_id'] = cart.id
        request.session.modified = True
    return cart


def my_cart_view(request):
    cart = get_or_create_cart(request)
    cart_items = CartItem.objects.filter(cart=cart)

    total = 0
    items = []

    for item in cart_items:
        unit_price = item.product.bulk_price if item.quantity >= 10 else item.product.price
        total_price = unit_price * item.quantity
        total += total_price

        items.append({
            'id': item.id,
            'product': item.product,
            'quantity': item.quantity,
            'unit_price': unit_price,
            'total_price': total_price
        })

    return render(request, 'mycart.html', {
        'cart_items': items,
        'total': total
    })


def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = get_or_create_cart(request)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('my_cart')

def update_cart_item(request, item_id):
    if request.method == 'POST':
        action = request.POST.get('action')
        cart_item = get_object_or_404(CartItem, id=item_id)

        if action == 'increment':
            cart_item.quantity += 1
        elif action == 'decrement' and cart_item.quantity > 1:
            cart_item.quantity -= 1

        cart_item.save()
    return redirect('my_cart')

def remove_cart_item(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)
    cart_item.delete()
    return redirect('my_cart')




def billing_view(request):
    cart = get_or_create_cart(request)
    cart_items = CartItem.objects.filter(cart=cart)

    total = 0
    items = []

    for item in cart_items:
        product = item.product
        unit_price = product.bulk_price if item.quantity >= 10 else product.price
        item_total = unit_price * item.quantity
        total += item_total

        items.append({
            'product': product,
            'quantity': item.quantity,
            'unit_price': unit_price,
            'total_price': item_total
        })

    if request.method == 'POST':
        form = BillingForm(request.POST)
        if form.is_valid():
            # ✅ Create Order
            order = Order.objects.create()  # you can add billing info here

            for item in cart_items:
                order_item = OrderItem.objects.create(
                    product=item.product,
                    quantity=item.quantity
                )
                order.items.add(order_item)

            cart_items.delete()
            messages.success(request, "Order placed successfully!")

            # ✅ Redirect to order detail page
            return redirect('myorder', order_id=order.id)
    else:
        form = BillingForm()

    return render(request, 'billing.html', {
        'form': form,
        'cart_items': items,
        'total': total
    })



def myorder_view(request, order_id):
    order = Order.objects.get(pk=order_id)
    return render(request, 'myorder.html', {'order': order})


def myorder_list_view(request):
    orders = Order.objects.all()  # or filter by user, if applicable
    return render(request, 'myorder_detail.html', {'order': orders})


def track_order_view(request):
    return render(request, 'track.html')

