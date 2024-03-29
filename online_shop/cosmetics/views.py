from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db import connection
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.utils import timezone
from .models import Category, Subcategory, Manufacturer, Product, Order, Cart, Client
from .forms import CategoryForm, SubcategoryForm, ManufacturerForm, ProductForm, OrderForm, \
    ShippingForm, SimpleDynamicQuery1Form, SimpleDynamicQuery2Form, SimpleDynamicQuery3Form, \
    SimpleDynamicQuery4Form, SimpleDynamicQuery5Form, SimpleDynamicQuery6Form, \
    SimpleDynamicQuery7Form, ComplexDynamicQueryForm, ComplexDynamicQuery1Form, \
    MonthlyOrderForm


def home(request):
    context = {
        'categories': Category.objects.raw("SELECT * FROM cosmetics_category"),
        'products': Product.objects.raw("SELECT * FROM cosmetics_product LIMIT 4")
    }
    return render(request, "cosmetics/home.html", context)


def categories(request):
    context = {
        'categories': Category.objects.raw("SELECT * FROM cosmetics_category"),
        'subcategories': Subcategory.objects.raw("SELECT * FROM cosmetics_subcategory"),
        'manufacturers': Manufacturer.objects.raw("SELECT * FROM cosmetics_manufacturer"),
        'products': Product.objects.raw("SELECT * FROM cosmetics_product"),
        'total_products': len(Product.objects.raw("SELECT * FROM cosmetics_product")),
        'category_id': 1
    }
    return render(request, "cosmetics/categories.html", context)


def products_from_category(request, id, sort):
    products_query = """ SELECT * 
    FROM cosmetics_product p 
    JOIN cosmetics_category c ON p.category_id=c.id 
    WHERE c.id=%s1
    ORDER BY p.price %s2;
    """
    query = products_query.replace('%s1', str(id))
    response = Product.objects.raw(query.replace('%s2', sort))

    context = {
        'categories': Category.objects.raw("SELECT * FROM cosmetics_category"),
        'subcategories': Subcategory.objects.raw("SELECT * FROM cosmetics_subcategory"),
        'manufacturers': Manufacturer.objects.raw("SELECT * FROM cosmetics_manufacturer"),
        'products': response,
        'total_products': len(response),
        'category_id': id
    }
    return render(request, "cosmetics/categories.html", context)


def products_from_subcategory(request, id):
    products_query = """ SELECT * 
                FROM cosmetics_product p 
                JOIN cosmetics_subcategory s ON p.subcategory_id=s.id 
                WHERE s.id=%s; """
    response = Product.objects.raw(products_query.replace('%s', str(id)))
    context = {
        'categories': Category.objects.raw("SELECT * FROM cosmetics_category"),
        'subcategories': Subcategory.objects.raw("SELECT * FROM cosmetics_subcategory"),
        'manufacturers': Manufacturer.objects.raw("SELECT * FROM cosmetics_manufacturer"),
        'products': response,
        'total_products': len(response),
        'category_id': id
    }
    return render(request, "cosmetics/categories.html", context)


def products_from_manufacturer(request, id):
    products_query = """ SELECT * 
                FROM cosmetics_product p 
                JOIN cosmetics_manufacturer m ON p.manufacturer_id=m.id 
                WHERE m.id=%s; """
    response = Product.objects.raw(products_query.replace('%s', str(id)))
    context = {
        'categories': Category.objects.raw("SELECT * FROM cosmetics_category"),
        'subcategories': Subcategory.objects.raw("SELECT * FROM cosmetics_subcategory"),
        'manufacturers': Manufacturer.objects.raw("SELECT * FROM cosmetics_manufacturer"),
        'products': response,
        'total_products': len(response),
        'category_id': id
    }
    return render(request, "cosmetics/categories.html", context)


def management(request):
    return render(request, "cosmetics/base_management.html")


def simple_dynamic_queries(request):
    if request.method == 'POST':
        form_query_1 = SimpleDynamicQuery1Form(request.POST)
        if form_query_1.is_valid():
            category_name = form_query_1.cleaned_data["category_name"]

            query_1 = """ SELECT p.name, c.name 
            FROM cosmetics_product p 
            JOIN cosmetics_category c ON p.category_id=c.id 
            WHERE c.name=%s; """
            with connection.cursor() as cursor:
                cursor.execute(query_1, [category_name])
                response_query_1 = cursor.fetchall()

            # Create a success notification to be displayed on the page
            messages.success(request, f"Query has been executed! Result {response_query_1}")
            context = {
                'form_query_1': form_query_1,
                'form_query_2': SimpleDynamicQuery2Form(),
                'form_query_3': SimpleDynamicQuery3Form(),
                'form_query_4': SimpleDynamicQuery4Form(),
                'form_query_5': SimpleDynamicQuery5Form(),
                'form_query_6': SimpleDynamicQuery6Form(),
                'form_query_7': SimpleDynamicQuery7Form(),
                'query_1': query_1.replace('%s', category_name),
                'response_query_1': response_query_1,
            }
            return render(request, 'cosmetics/management/simple_dynamic_query.html', context)

        form_query_2 = SimpleDynamicQuery2Form(request.POST)
        if form_query_2.is_valid():
            manufacturer_name = form_query_2.cleaned_data["manufacturer_name"]

            query_2 = """ SELECT p.name, m.name 
            FROM cosmetics_product p 
            JOIN cosmetics_manufacturer m ON p.manufacturer_id=m.id 
            WHERE m.name=%s; """
            with connection.cursor() as cursor:
                cursor.execute(query_2, [manufacturer_name])
                response_query_2 = cursor.fetchall()

            # Create a success notification to be displayed on the page
            messages.success(request, f"Query has been executed! Result {response_query_2}")
            context = {
                'form_query_1': SimpleDynamicQuery1Form(),
                'form_query_2': form_query_2,
                'form_query_3': SimpleDynamicQuery3Form(),
                'form_query_4': SimpleDynamicQuery4Form(),
                'form_query_5': SimpleDynamicQuery5Form(),
                'form_query_6': SimpleDynamicQuery6Form(),
                'form_query_7': SimpleDynamicQuery7Form(),
                'query_2': query_2.replace('%s', manufacturer_name),
                'response_query_2': response_query_2,
            }
            return render(request, 'cosmetics/management/simple_dynamic_query.html', context)

        form_query_3 = SimpleDynamicQuery3Form(request.POST)
        if form_query_3.is_valid():
            product_quantity = form_query_3.cleaned_data["product_quantity"]

            query_3 = """ SELECT p.name, p.quantity 
            FROM cosmetics_product p 
            WHERE p.quantity < %s ;"""
            with connection.cursor() as cursor:
                cursor.execute(query_3, [int(product_quantity)])
                response_query_3 = cursor.fetchall()

            # Create a success notification to be displayed on the page
            messages.success(request, f"Query has been executed! Result {response_query_3}")
            context = {
                'form_query_1': SimpleDynamicQuery1Form(),
                'form_query_2': SimpleDynamicQuery2Form(),
                'form_query_3': form_query_3,
                'form_query_4': SimpleDynamicQuery4Form(),
                'form_query_5': SimpleDynamicQuery5Form(),
                'form_query_6': SimpleDynamicQuery6Form(),
                'form_query_7': SimpleDynamicQuery7Form(),
                'query_3': query_3.replace('%s', str(product_quantity)),
                'response_query_3': response_query_3,
            }
            return render(request, 'cosmetics/management/simple_dynamic_query.html', context)

        form_query_4 = SimpleDynamicQuery4Form(request.POST)
        if form_query_4.is_valid():
            start_date = form_query_4.cleaned_data["start_date"]
            stop_date = form_query_4.cleaned_data["stop_date"]

            query_4 = """ SELECT c.username, o.ordered_date 
            FROM cosmetics_order o 
            JOIN cosmetics_client c ON c.id=o.client_id 
            WHERE o.ordered_date BETWEEN %s1 AND %s2;"""
            with connection.cursor() as cursor:
                cursor.execute(query_4, [start_date, stop_date])
                response_query_4 = cursor.fetchall()

            # Create a success notification to be displayed on the page
            messages.success(request, f"Query has been executed! Result {response_query_4}")
            context = {
                'form_query_1': SimpleDynamicQuery1Form(),
                'form_query_2': SimpleDynamicQuery2Form(),
                'form_query_3': SimpleDynamicQuery3Form(),
                'form_query_4': form_query_4,
                'form_query_5': SimpleDynamicQuery5Form(),
                'form_query_6': SimpleDynamicQuery6Form(),
                'form_query_7': SimpleDynamicQuery7Form(),
                'query_4': query_4.replace('%s1', str(start_date)).replace('%s2', str(stop_date)),
                'response_query_4': response_query_4,
            }
            return render(request, 'cosmetics/management/simple_dynamic_query.html', context)

        form_query_5 = SimpleDynamicQuery5Form(request.POST)
        if form_query_5.is_valid():
            new_category_name = form_query_5.cleaned_data["new_category_name"]

            query_5 = """ SELECT s.name, c.name 
            FROM cosmetics_subcategory s 
            JOIN cosmetics_category c ON s.category_id=c.id 
            WHERE c.name=%s; """
            with connection.cursor() as cursor:
                cursor.execute(query_5, [new_category_name])
                response_query_5 = cursor.fetchall()

            # Create a success notification to be displayed on the page
            messages.success(request, f"Query has been executed! Result {response_query_5}")
            context = {
                'form_query_1': SimpleDynamicQuery1Form(),
                'form_query_2': SimpleDynamicQuery2Form(),
                'form_query_3': SimpleDynamicQuery3Form(),
                'form_query_4': SimpleDynamicQuery4Form(),
                'form_query_5': form_query_5,
                'form_query_6': SimpleDynamicQuery6Form(),
                'form_query_7': SimpleDynamicQuery7Form(),
                'query_5': query_5.replace('%s', new_category_name),
                'response_query_5': response_query_5,
            }
            return render(request, 'cosmetics/management/simple_dynamic_query.html', context)

        form_query_6 = SimpleDynamicQuery6Form(request.POST)
        if form_query_6.is_valid():
            product_price = form_query_6.cleaned_data["product_price"]

            query_6 = """ SELECT p.name, p.price 
            FROM cosmetics_product p 
            WHERE p.price < %s ;"""
            with connection.cursor() as cursor:
                cursor.execute(query_6, [int(product_price)])
                response_query_6 = cursor.fetchall()

            # Create a success notification to be displayed on the page
            messages.success(request, f"Query has been executed! Result {response_query_6}")
            context = {
                'form_query_1': SimpleDynamicQuery1Form(),
                'form_query_2': SimpleDynamicQuery2Form(),
                'form_query_3': SimpleDynamicQuery3Form(),
                'form_query_4': SimpleDynamicQuery4Form(),
                'form_query_5': SimpleDynamicQuery5Form(),
                'form_query_6': form_query_6,
                'form_query_7': SimpleDynamicQuery7Form(),
                'query_6': query_6.replace('%s', str(product_price)),
                'response_query_6': response_query_6,
            }
            return render(request, 'cosmetics/management/simple_dynamic_query.html', context)

        form_query_7 = SimpleDynamicQuery7Form(request.POST)
        if form_query_7.is_valid():
            status_order = form_query_7.cleaned_data["status_order"]

            query_7 = """ SELECT c.username, o.status
            FROM cosmetics_order o
            JOIN cosmetics_client c ON c.id=o.client_id 
            WHERE o.status = %s ;"""
            with connection.cursor() as cursor:
                cursor.execute(query_7, [status_order])
                response_query_7 = cursor.fetchall()

            # Create a success notification to be displayed on the page
            messages.success(request, f"Query has been executed! Result {response_query_7}")
            context = {
                'form_query_1': SimpleDynamicQuery1Form(),
                'form_query_2': SimpleDynamicQuery2Form(),
                'form_query_3': SimpleDynamicQuery3Form(),
                'form_query_4': SimpleDynamicQuery4Form(),
                'form_query_5': SimpleDynamicQuery5Form(),
                'form_query_6': SimpleDynamicQuery6Form(),
                'form_query_7': form_query_7,
                'query_7': query_7.replace('%s', str(status_order)),
                'response_query_7': response_query_7,
            }
            return render(request, 'cosmetics/management/simple_dynamic_query.html', context)

    else:
        context = {
            'form_query_1': SimpleDynamicQuery1Form(),
            'form_query_2': SimpleDynamicQuery2Form(),
            'form_query_3': SimpleDynamicQuery3Form(),
            'form_query_4': SimpleDynamicQuery4Form(),
            'form_query_5': SimpleDynamicQuery5Form(),
            'form_query_6': SimpleDynamicQuery6Form(),
            'form_query_7': SimpleDynamicQuery7Form(),
        }
    return render(request, 'cosmetics/management/simple_dynamic_query.html', context)


def simple_queries(request):
    query_1 = """ SELECT p.name, c.name 
    FROM cosmetics_product p 
    JOIN cosmetics_category c ON p.category_id=c.id 
    WHERE c.name='Make-up'; """
    query_2 = """ SELECT p.name, m.name 
    FROM cosmetics_product p 
    JOIN cosmetics_manufacturer m ON p.manufacturer_id=m.id 
    WHERE m.name='Bioderma'; """
    query_3 = """ SELECT p.name, p.quantity 
    FROM cosmetics_product p 
    WHERE p.quantity < 100 ;"""
    query_4 = """ SELECT c.username, o.ordered_date 
    FROM cosmetics_order o 
    JOIN cosmetics_client c ON c.id=o.client_id 
    WHERE o.ordered_date BETWEEN '2024-01-01' AND '2024-06-06';"""
    query_5 = """ SELECT s.name, c.name 
    FROM cosmetics_subcategory s 
    JOIN cosmetics_category c ON s.category_id=c.id 
    WHERE c.name='Skin-care'; """
    query_6 = """ SELECT p.name, p.price 
    FROM cosmetics_product p 
    WHERE p.price < 100 ;"""
    query_7 = """ SELECT c.username, o.status
    FROM cosmetics_order o
    JOIN cosmetics_client c ON c.id=o.client_id 
    WHERE o.status = 'FI' ;"""
    with connection.cursor() as cursor:
        cursor.execute(query_1)
        response_query_1 = cursor.fetchall()
        cursor.execute(query_2)
        response_query_2 = cursor.fetchall()
        cursor.execute(query_3)
        response_query_3 = cursor.fetchall()
        cursor.execute(query_4)
        response_query_4 = cursor.fetchall()
        cursor.execute(query_5)
        response_query_5 = cursor.fetchall()
        cursor.execute(query_6)
        response_query_6 = cursor.fetchall()
        cursor.execute(query_7)
        response_query_7 = cursor.fetchall()

    context = {
        'query_1': query_1,
        'response_query_1': response_query_1,
        'query_2': query_2,
        'response_query_2': response_query_2,
        'query_3': query_3,
        'response_query_3': response_query_3,
        'query_4': query_4,
        'response_query_4': response_query_4,
        'query_5': query_5,
        'response_query_5': response_query_5,
        'query_6': query_6,
        'response_query_6': response_query_6,
        'query_7': query_7,
        'response_query_7': response_query_7,
    }
    return render(request, 'cosmetics/management/simple_query.html', context)


def complex_queries(request):
    if request.method == 'POST':
        form_complex_query_1 = ComplexDynamicQuery1Form(request.POST)
        if form_complex_query_1.is_valid():
            category_name = form_complex_query_1.cleaned_data["category_name"]

            complex_query_1 = """ SELECT cl.username
            FROM cosmetics_client cl
            WHERE cl.id IN (
                SELECT DISTINCT co.client_id
                FROM cosmetics_order co
                WHERE co.client_id NOT IN (
                    SELECT DISTINCT co.client_id
                    FROM cosmetics_order co
                    JOIN cosmetics_cart ccart ON co.id = ccart.ordered
                    JOIN cosmetics_product cp ON ccart.product_id = cp.id
                    JOIN cosmetics_subcategory cs ON cp.subcategory_id = cs.id
                    JOIN cosmetics_category cc ON cp.category_id = cc.id
                    WHERE cc.name = %s
                )
                AND co.client_id IN (
                    SELECT DISTINCT co.client_id
                    FROM cosmetics_order co
                    JOIN cosmetics_cart ccart ON co.id = ccart.ordered
                    JOIN cosmetics_product cp ON ccart.product_id = cp.id
                    JOIN cosmetics_subcategory cs ON cp.subcategory_id = cs.id
                    GROUP BY co.client_id
                    HAVING COUNT(DISTINCT cs.id) > 1
                )
            );"""
            with connection.cursor() as cursor:
                cursor.execute(complex_query_1, [category_name])
                response_query_1 = cursor.fetchall()

            print(response_query_1)
            # Create a success notification to be displayed on the page
            messages.success(request, f"Query has been executed! Result {response_query_1}")
            context = {
                'form_complex_query_1': form_complex_query_1,
                'complex_query_1': complex_query_1.replace('%s', category_name),
                'response_query_1': response_query_1,
            }
            return render(request, 'cosmetics/management/complex_query.html', context)

    else:

        complex_query_2 = """ SELECT cp.name AS product_name, cc.name AS category_name, SUM(ccart.quantity) AS total_purchases
        FROM cosmetics_cart ccart
        JOIN cosmetics_product cp ON ccart.product_id = cp.id
        JOIN cosmetics_category cc ON cp.category_id = cc.id
        GROUP BY cp.name
        HAVING SUM(ccart.quantity) = (
            SELECT MAX(total_purchases)
            FROM (
                SELECT cp.category_id, cp.id AS product_id, SUM(ccart.quantity) AS total_purchases
                FROM cosmetics_cart ccart
                JOIN cosmetics_product cp ON ccart.product_id = cp.id
                JOIN cosmetics_category cc ON cp.category_id = cc.id
                GROUP BY cp.category_id, cp.id
            ) AS category_product_purchases
            WHERE category_product_purchases.category_id = cp.category_id
        ); """

        complex_query_3 = """ SELECT cl.username,
        client_spending.total_spent_cat_1 AS total_spent_category_1,
        client_spending.total_spent_cat_2 AS total_spent_category_2
        FROM cosmetics_client cl
        JOIN (
            SELECT co.client_id,
                SUM(CASE WHEN cp.category_id = 3 THEN ccart.quantity * cp.price ELSE 0 END) AS total_spent_cat_1,
                SUM(CASE WHEN cp.category_id = 4 THEN ccart.quantity * cp.price ELSE 0 END) AS total_spent_cat_2
            FROM cosmetics_order co
            JOIN cosmetics_cart ccart ON co.id = ccart.ordered
            JOIN cosmetics_product cp ON ccart.product_id = cp.id
            GROUP BY co.client_id
        ) AS client_spending ON cl.id = client_spending.client_id
        WHERE client_spending.total_spent_cat_1 > client_spending.total_spent_cat_2;"""

        with connection.cursor() as cursor:
            cursor.execute(complex_query_2)
            response_query_2 = cursor.fetchall()
            cursor.execute(complex_query_3)
            response_query_3 = cursor.fetchall()

        context = {
            'form_complex_query_1': ComplexDynamicQuery1Form(),
            'complex_query_2': complex_query_2,
            'response_query_2': response_query_2,
            'complex_query_3': complex_query_3,
            'response_query_3': response_query_3,
        }

    return render(request, 'cosmetics/management/complex_query.html', context)


@login_required
def view_cart(request):
    try:
        order = Order.objects.get(client=request.user, ordered=False)
        context = {
            'order': order
        }
        return render(request, "cosmetics/cart.html", context)
    except ObjectDoesNotExist:
        messages.warning(request, "You do not have an active order")
        return redirect("home")


@login_required
def add_to_cart(request, id):
    product = get_object_or_404(Product, pk=id)
    cart_item, created = Cart.objects.get_or_create(client=request.user, product=product, ordered=False)

    order_qs = Order.objects.filter(client=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.carts.filter(product_id=product.id).exists():
            cart_item.quantity += 1
            cart_item.save()
            messages.info(request, "This product quantity was updated.")
            return redirect('view_cart')
        else:
            order.carts.add(cart_item)
            messages.success(request, "This item was added to your cart.")
            return redirect('view_cart')
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(client=request.user, ordered_date=ordered_date)
        order.save()
        order.carts.add(cart_item)
        messages.success(request, "This item was added to your cart.")
        return redirect('view_cart')


@login_required
def remove_from_cart(request, id):
    product = get_object_or_404(Product, pk=id)
    order_qs = Order.objects.filter(client=request.user, ordered=False)

    if order_qs.exists():
        order = order_qs[0]
        if order.carts.filter(product_id=product.id).exists():
            cart_item = Cart.objects.filter(client=request.user, product=product, ordered=False)[0]
            order.carts.remove(cart_item)
            cart_item.delete()
            messages.info(request, "This item was removed from your cart.")
            return redirect('view_cart')
        else:
            messages.info(request, "This item was not in your cart")
            return redirect('categories')
    else:
        messages.info(request, "You do not have an active order")
        return redirect('categories')


@login_required
def view_checkout(request):

    if request.method == 'POST':
        shipping_form = ShippingForm(data=request.POST or None)
        try:
            order = Order.objects.get(client=request.user, ordered=False)

            # shipping_form = ShippingForm(data=request.POST, instance=order)
            if shipping_form.is_valid():
                order.status = "PR"
                order.save()
                # order.carts.set(items)
                street = shipping_form.cleaned_data["street"]
                city = shipping_form.cleaned_data["city"]
                country = shipping_form.cleaned_data["country"]
                zip_code = shipping_form.cleaned_data["zip_code"]

                ordered_date = timezone.now()

                # Update ordered status for cart items
                order_carts = order.carts.all()
                order.carts.update(ordered=True)
                for item in order_carts:
                    item.save()

                # Update ordered status for order item
                order.ordered = True
                order.save()

                # Update using Django syntax
                # order.ordered_date = ordered_date
                # order.save()
                # shipping_form.save()

                # Update and get object using SQL syntax
                with connection.cursor() as cursor:
                    cursor.execute("UPDATE cosmetics_order SET "
                                   "street=%s, city=%s, country=%s, "
                                   "zip_code=%s, ordered_date=%s WHERE id=%s",
                                   [street, city, country, zip_code, ordered_date, order.id])
                    cursor.execute("SELECT * FROM cosmetics_order WHERE id=%s", [order.id])

                # Create a success notification to be displayed on the page
                messages.success(request, f"Order {order.id} has been sent!")
                return redirect('categories')
        except ObjectDoesNotExist:
            messages.info(request, "You do not have an active order")
            return redirect('categories')
    else:
        try:
            # Get object from database using Django syntax
            order = Order.objects.get(client=request.user, ordered=False)

            context = {
                'shipping_form': ShippingForm(),
                'order': order,
            }
            return render(request, "cosmetics/checkout.html", context)
        except ObjectDoesNotExist:
            messages.info(request, "You do not have an active order")
            return redirect('home')
            # Order.objects.create(client=request.user, status='AW')

    return redirect('view_checkout')


def manage_order(request):
    order_form = OrderForm()
    orders = Order.objects.raw("SELECT * FROM cosmetics_order")
    context = {
        'order_form': order_form,
        'orders': orders,
    }
    return render(request, 'cosmetics/management/order.html', context)


def delete_order(request, id):
    # Delete using Django syntax
    Order.objects.filter(id=id).delete()
    messages.success(request, f"Order number {id} has been deleted!")
    return redirect('manage_order')


def update_order(request, id):
    # Get object from database using Django syntax
    order = get_object_or_404(Order, pk=id)

    if request.method == 'POST':
        order_form = OrderForm(data=request.POST, instance=order)
        if order_form.is_valid():
            status = order_form.cleaned_data["status"]
            street = order_form.cleaned_data["street"]
            city = order_form.cleaned_data["city"]
            country = order_form.cleaned_data["country"]
            zip_code = order_form.cleaned_data["zip_code"]

            # Update using Django syntax
            # order_form.save()

            # Update and get object using SQL syntax
            with connection.cursor() as cursor:
                cursor.execute("UPDATE cosmetics_order SET status=%s,"
                               "street=%s, city=%s, country=%s, zip_code=%s WHERE id=%s",
                               [status, street, city, country, zip_code, order.pk])
                cursor.execute("SELECT * FROM cosmetics_order WHERE id=%s", [id])

            # Create a warning notification to be displayed on the page
            messages.warning(request, f"Order number {id} has been updated!")
            return redirect('manage_order')
    else:
        order_form = OrderForm(instance=order)
    context = {
        'order_form': order_form,
        'orders': Order.objects.raw("SELECT * FROM cosmetics_order"),
    }
    return render(request, 'cosmetics/management/order.html', context)


@login_required
def user_profile(request):

    context = {
        'client': Client.objects.raw("SELECT * FROM cosmetics_client WHERE username=%s", [str(request.user)])[0],
        'orders': Order.objects.raw("SELECT * FROM cosmetics_order WHERE client_id=%s", [str(request.user.id)]),
    }

    return render(request, 'cosmetics/user_profile.html', context)


def manage_category(request):
    if request.method == "POST":
        # Initialize form for category
        category_form = CategoryForm(request.POST, request.FILES)
        context = {
            'category_form': category_form
        }
        if category_form.is_valid():
            # Get data from web interface
            name = category_form.cleaned_data["name"]

            # Create a new object to be inserted in database
            model_category = Category(name=name, icon=request.FILES["icon"])

            # Save the object in database with the above values
            model_category.save()

            # Get list of categories from database
            context['categories'] = Category.objects.raw("SELECT * FROM cosmetics_category")

            # Create a successful notification to be displayed on the page
            messages.success(request, f"Category {name} has been created!")
            return redirect('manage_category')
        else:
            print("Category Form is invalid")
            # Create an error notification to be displayed on the page
            messages.error(request, "Inserted data are wrong! Please check again the data!")
    elif request.method == "GET":
        category_form = CategoryForm()
        context = {
            'category_form': category_form,
            'categories': Category.objects.raw("SELECT * FROM cosmetics_category"),
        }
    return render(request, 'cosmetics/management/category.html', context)


def delete_category(request, id):
    # Delete using Django syntax
    # Category.objects.filter(id=id).delete()

    # Delete using SQL syntax
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM cosmetics_category WHERE id=%s", [id])
    # Create a successful notification to be displayed on the page
    messages.success(request, f"Category with {id} has been deleted!")
    return redirect('manage_category')


def update_category(request, id):
    # Get object from database using Django syntax
    category = get_object_or_404(Category, id=id)

    if request.method == 'POST':
        category_form = CategoryForm(data=request.POST, instance=category)
        if category_form.is_valid():
            name = category_form.cleaned_data["name"]
            # Update using Django syntax
            # category_form.save()

            # Update and get object using SQL syntax
            with connection.cursor() as cursor:
                cursor.execute("UPDATE cosmetics_category SET name=%s WHERE id=%s", [name, id])
                cursor.execute("SELECT * FROM cosmetics_category WHERE id=%s", [id])

            # Create a warning notification to be displayed on the page
            messages.warning(request, f"Category {name} has been updated!")
            return redirect('manage_category')
    else:
        category_form = CategoryForm(instance=category)
    context = {
        'category_form': category_form,
        'categories': Category.objects.raw("SELECT * FROM cosmetics_category"),
    }
    return render(request, 'cosmetics/management/category.html', context)


def manage_subcategory(request):
    if request.method == "POST":
        # Initialize form for subcategory
        subcategory_form = SubcategoryForm(request.POST)
        context = {
            'subcategory_form': subcategory_form
        }
        if subcategory_form.is_valid():
            # Get data from web interface
            name = subcategory_form.cleaned_data["name"]
            category = subcategory_form.cleaned_data["category"]

            # Insert object using Django syntax
            # # Create a new object to be inserted in database
            # model_subcategory = Subcategory(name=name, category=category)
            #
            # # Save the object in database with the above values
            # model_subcategory.save()

            # Insert object using SQL syntax
            insert_query = "INSERT INTO cosmetics_subcategory(name, category_id) VALUES( %s, %s )"
            with connection.cursor() as cursor:
                cursor.execute(insert_query, [name, str(category.id)])

            # Get list of categories from database
            context['subcategories'] = Subcategory.objects.raw("SELECT * FROM cosmetics_subcategory")

            # Create a successful notification to be displayed on the page
            messages.success(request, f"Subcategory {name} has been created!")
            return redirect('manage_subcategory')
        else:
            print("subcategory Form is invalid")
            # Create an error notification to be displayed on the page
            messages.error(request, "Inserted data are wrong! Please check again the data!")
    elif request.method == "GET":
        subcategory_form = SubcategoryForm()
        context = {
            'subcategory_form': subcategory_form,
            'subcategories': Subcategory.objects.raw("SELECT * FROM cosmetics_subcategory"),
        }
    return render(request, 'cosmetics/management/subcategory.html', context)


def delete_subcategory(request, id):
    # Delete using Django syntax
    # subcategory.objects.filter(id=id).delete()

    # Delete using SQL syntax
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM cosmetics_subcategory WHERE id=%s", [id])
    # Create a successful notification to be displayed on the page
    messages.success(request, f"Subcategory with {id} has been deleted!")
    return redirect('manage_subcategory')


def update_subcategory(request, id):
    # Get object from database using Django syntax
    subcategory = get_object_or_404(Subcategory, id=id)

    if request.method == 'POST':
        subcategory_form = SubcategoryForm(data=request.POST, instance=subcategory)
        if subcategory_form.is_valid():
            name = subcategory_form.cleaned_data["name"]
            # Update using Django syntax
            # subcategory_form.save()

            # Update and get object using SQL syntax
            with connection.cursor() as cursor:
                cursor.execute("UPDATE cosmetics_subcategory SET name=%s WHERE id=%s", [name, id])
                cursor.execute("SELECT * FROM cosmetics_subcategory WHERE id=%s", [id])

            # Create a warning notification to be displayed on the page
            messages.warning(request, f"Subcategory {name} has been updated!")
            return redirect('manage_subcategory')
    else:
        subcategory_form = SubcategoryForm(instance=subcategory)
    context = {
        'subcategory_form': subcategory_form,
        'subcategories': Subcategory.objects.raw("SELECT * FROM cosmetics_subcategory"),
    }
    return render(request, 'cosmetics/management/subcategory.html', context)


def manage_manufacturer(request):
    if request.method == "POST":
        # Initialize form for manufacturer
        manufacturer_form = ManufacturerForm(request.POST)
        context = {
            'manufacturer_form': manufacturer_form
        }
        if manufacturer_form.is_valid():
            # Get data from web interface
            name = manufacturer_form.cleaned_data["name"]

            # Insert object using Django syntax
            # # Create a new object to be inserted in database
            # model_manufacturer = Manufacturer(name=name)
            #
            # # Save the object in database with the above values
            # model_manufacturer.save()

            # Insert object using SQL syntax
            insert_query = "INSERT INTO cosmetics_manufacturer(name) VALUES( %s )"
            with connection.cursor() as cursor:
                cursor.execute(insert_query, [name])

            # Get list of categories from database
            context['manufacturers'] = Manufacturer.objects.raw("SELECT * FROM cosmetics_manufacturer")

            # Create a successful notification to be displayed on the page
            messages.success(request, f"Manufacturer {name} has been created!")
            return redirect('manage_manufacturer')
        else:
            print("Manufacturer Form is invalid")
            # Create an error notification to be displayed on the page
            messages.error(request, "Inserted data are wrong! Please check again the data!")
    elif request.method == "GET":
        manufacturer_form = ManufacturerForm()
        context = {
            'manufacturer_form': manufacturer_form,
            'manufacturers': Manufacturer.objects.raw("SELECT * FROM cosmetics_manufacturer"),
        }
    return render(request, 'cosmetics/management/manufacturer.html', context)


def delete_manufacturer(request, id):
    # Delete using Django syntax
    # Manufacturer.objects.filter(id=id).delete()

    # Delete using SQL syntax
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM cosmetics_manufacturer WHERE id=%s", [id])
    # Create a successful notification to be displayed on the page
    messages.success(request, f"Manufacturer with {id} has been deleted!")
    return redirect('manage_manufacturer')


def update_manufacturer(request, id):
    # Get object from database using Django syntax
    manufacturer = get_object_or_404(Manufacturer, id=id)

    if request.method == 'POST':
        manufacturer_form = ManufacturerForm(data=request.POST, instance=manufacturer)
        if manufacturer_form.is_valid():
            name = manufacturer_form.cleaned_data["name"]
            # Update using Django syntax
            # manufacturer_form.save()

            # Update and get object using SQL syntax
            with connection.cursor() as cursor:
                cursor.execute("UPDATE cosmetics_manufacturer SET name=%s WHERE id=%s", [name, id])
                cursor.execute("SELECT * FROM cosmetics_manufacturer WHERE id=%s", [id])

            # Create a warning notification to be displayed on the page
            messages.warning(request, f"Manufacturer {name} has been updated!")
            return redirect('manage_manufacturer')
    else:
        manufacturer_form = ManufacturerForm(instance=manufacturer)
    context = {
        'manufacturer_form': manufacturer_form,
        'manufacturers': Manufacturer.objects.raw("SELECT * FROM cosmetics_manufacturer"),
    }
    return render(request, 'cosmetics/management/manufacturer.html', context)


def manage_product(request):
    if request.method == "POST":
        # Initialize form for product
        product_form = ProductForm(request.POST, request.FILES)
        context = {
            'product_form': product_form
        }
        if product_form.is_valid():
            # Get data from web interface
            name = product_form.cleaned_data["name"]
            description = product_form.cleaned_data["description"]
            price = product_form.cleaned_data["price"]
            quantity = product_form.cleaned_data["quantity"]
            category = product_form.cleaned_data["category"]
            subcategory = product_form.cleaned_data["subcategory"]
            manufacturer = product_form.cleaned_data["manufacturer"]

            # Create a new object to be inserted in database
            model_product = Product(name=name,
                                    description=description,
                                    price=price,
                                    quantity=quantity,
                                    icon=request.FILES["icon"],
                                    category=category,
                                    subcategory=subcategory,
                                    manufacturer=manufacturer)

            # Save the object in database with the above values
            model_product.save()

            # Get list of categories from database
            context['products'] = Product.objects.raw("SELECT * FROM cosmetics_product")

            # Create a successful notification to be displayed on the page
            messages.success(request, f"Product {name} has been created!")
            return redirect('manage_product')
        else:
            print("Product Form is invalid")

            # Create an error notification to be displayed on the page
            messages.error(request, "Inserted data are wrong! Please check again the data!")
    elif request.method == "GET":
        product_form = ProductForm()
        context = {
            'product_form': product_form,
            'products': Product.objects.raw("SELECT * FROM cosmetics_product"),
        }
    return render(request, 'cosmetics/management/product.html', context)


def delete_product(request, id):
    # Delete using Django syntax
    # Product.objects.filter(id=id).delete()

    # Delete using SQL syntax
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM cosmetics_product WHERE id=%s", [id])
    # Create a successful notification to be displayed on the page
    messages.success(request, f"Product with {id} has been deleted!")
    return redirect('manage_product')


def update_product(request, id):
    product = get_object_or_404(Product, id=id)
    if request.method == 'POST':
        product_form = ProductForm(data=request.POST, instance=product)
        if product_form.is_valid():
            name = product_form.cleaned_data["name"]
            description = product_form.cleaned_data["description"]
            price = product_form.cleaned_data["price"]
            quantity = product_form.cleaned_data["quantity"]
            category = product_form.cleaned_data["category"]
            subcategory = product_form.cleaned_data["subcategory"]
            manufacturer = product_form.cleaned_data["manufacturer"]

            category_id = Category.objects.raw("SELECT * FROM cosmetics_category WHERE name=%s", [str(category)])
            subcategory_id = Subcategory.objects.raw("SELECT * FROM cosmetics_subcategory WHERE name=%s", [str(subcategory)])
            manufacturer_id = Manufacturer.objects.raw("SELECT * FROM cosmetics_manufacturer WHERE name=%s", [str(manufacturer)])

            # Update using Django syntax
            # product_form.save()

            # Update and get object using SQL syntax
            with connection.cursor() as cursor:
                cursor.execute("UPDATE cosmetics_product SET name=%s, description=%s, "
                               "price=%s, quantity=%s, category_id=%s, "
                               "subcategory_id=%s, manufacturer_id=%s WHERE id=%s",
                               [name, description, price, quantity,
                                category_id[0].id, subcategory_id[0].id, manufacturer_id[0].id, id])
                cursor.execute("SELECT * FROM cosmetics_product WHERE id=%s", [id])

            # For debug purposes
            # print(connection.queries)

            # Create a warning notification to be displayed on the page
            messages.warning(request, f"Product {name} has been updated!")
            return redirect('manage_product')
    else:
        product_form = ProductForm(instance=product)
    context = {
        'product_form': product_form,
        'products': Product.objects.raw("SELECT * FROM cosmetics_product"),
    }
    return render(request, 'cosmetics/management/product.html', context)


def statistics(request):
    month_income = 0
    vat_value = 0
    total_orders = 0
    if request.method == 'POST':
        monthly_form = MonthlyOrderForm(request.POST)
        if monthly_form.is_valid():
            month = monthly_form.cleaned_data["month"]

            orders_response_info = Order.objects.raw("SELECT * FROM cosmetics_order WHERE ordered_date BETWEEN '2024-%s-01' AND '2024-%s-30'".replace('%s', str(month)))
            for order in orders_response_info:
                month_income += order.get_total()
            orders_query = """ SELECT o.status, c.username, o.ordered_date
            FROM cosmetics_order o 
            JOIN cosmetics_client c ON c.id=o.client_id
            WHERE o.ordered_date BETWEEN '2024-%s-01' AND '2024-%s-30';"""

            with connection.cursor() as cursor:
                cursor.execute(orders_query.replace('%s', str(month)))
                orders_response = cursor.fetchall()

            all_orders = zip(orders_response, orders_response_info)

            context = {
                'monthly_form': monthly_form,
                'total_orders': len(orders_response),
                'all_orders': all_orders,
                'month_income': month_income,
                'vat': month_income*0.19,
                'average_price_order': month_income/len(orders_response) if len(orders_response) > 0 else total_orders,
                'category_form': ComplexDynamicQuery1Form(),
                'complex_form': ComplexDynamicQueryForm(),
            }

            return render(request, 'cosmetics/statistics.html', context)

        category_form = ComplexDynamicQuery1Form(request.POST)
        if category_form.is_valid():
            category_name = category_form.cleaned_data["category_name"]

            products_query = """ SELECT p.name, cc.name, cs.name, cm.name, SUM(c.quantity) as total_comandat, p.price
            FROM cosmetics_product p
            JOIN cosmetics_cart c ON p.id=c.product_id
            JOIN cosmetics_category cc on cc.id=p.category_id 
            JOIN cosmetics_subcategory cs on cs.id=p.subcategory_id 
            JOIN cosmetics_manufacturer cm on cm.id=p.manufacturer_id  	 
            WHERE cc.name = %s
            GROUP BY p.id
            ORDER BY total_comandat DESC; """

            with connection.cursor() as cursor:
                cursor.execute(products_query, [category_name])
                products_response = cursor.fetchall()

            context = {
                'monthly_form': MonthlyOrderForm(),
                'complex_form': ComplexDynamicQueryForm(),
                'total_orders': total_orders,
                'month_income': month_income,
                'vat': month_income*0.19,
                'average_price_order': total_orders,
                'category_form': category_form,
                'products': products_response,
            }

            return render(request, 'cosmetics/statistics.html', context)

        complex_form = ComplexDynamicQueryForm(request.POST)
        if complex_form.is_valid():
            subcategory_name = complex_form.cleaned_data["subcategory_name"]

            complex_query = """ SELECT cl.username, cp.name AS product_name, cp.price, ccart.quantity, co.ordered_date
            FROM cosmetics_cart ccart
            JOIN cosmetics_product cp ON ccart.product_id = cp.id
            JOIN cosmetics_order co ON ccart.ordered = co.id
            JOIN cosmetics_client cl ON co.client_id = cl.id
            JOIN cosmetics_subcategory cs ON cp.subcategory_id = cs.id
            JOIN (
                SELECT cp.subcategory_id, MAX(cp.price) - MIN(cp.price) AS price_range
                FROM cosmetics_product cp
                GROUP BY cp.subcategory_id
            ) AS subcategory_price_range ON cs.id = subcategory_price_range.subcategory_id
            WHERE cs.name = %s
            ORDER BY cl.last_name, cl.first_name, cp.name, co.ordered_date;"""

            with connection.cursor() as cursor:
                cursor.execute(complex_query, [subcategory_name])
                complex_response = cursor.fetchall()

            context = {
                'monthly_form': MonthlyOrderForm(),
                'total_orders': total_orders,
                'month_income': month_income,
                'vat': month_income*0.19,
                'average_price_order': total_orders,
                'category_form': ComplexDynamicQuery1Form(),
                'complex_form': complex_form,
                'complex_response': complex_response,
            }

            return render(request, 'cosmetics/statistics.html', context)

    else:
        context = {
            'monthly_form': MonthlyOrderForm(),
            'category_form': ComplexDynamicQuery1Form(),
            'complex_form': ComplexDynamicQueryForm(),
            'total_orders': total_orders,
            'month_income': month_income,
            'vat': vat_value
        }
    return render(request, 'cosmetics/statistics.html', context)


def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    context = {
        'product': product,
    }
    return render(request, 'cosmetics/product_detail.html', context)

