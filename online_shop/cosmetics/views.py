from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest, HttpResponse
from django.db import connection
from django.contrib import messages
from .models import Category, Manufacturer, Product
from .forms import CategoryForm, ManufacturerForm, ProductForm


def home(request):
    context = {
        'categories': Category.objects.raw("SELECT * FROM cosmetics_category")
    }
    return render(request, "cosmetics/home.html", context)


def categories(request):
    context = {
        'categories': Category.objects.raw("SELECT * FROM cosmetics_category"),
        'products': Product.objects.raw("SELECT * FROM cosmetics_product"),
    }
    return render(request, "cosmetics/categories.html", context)


def management(request):
    return render(request, "cosmetics/base_management.html")


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
    category = get_object_or_404(Category, id=id)
    if request.method == 'POST':
        category_form = CategoryForm(data=request.POST, instance=category)
        if category_form.is_valid():
            category_form.save()
            name = category_form.cleaned_data["name"]

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


def manage_manufacturer(request):
    if request.method == "POST":
        # Initialize form for category
        manufacturer_form = ManufacturerForm(request.POST)
        context = {
            'manufacturer_form': manufacturer_form
        }
        if manufacturer_form.is_valid():
            # Get data from web interface
            name = manufacturer_form.cleaned_data["name"]

            # Create a new object to be inserted in database
            model_manufacturer = Manufacturer(name=name)

            # Save the object in database with the above values
            model_manufacturer.save()

            # Get list of categories from database
            context['manufacturers'] = Manufacturer.objects.values()

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
            'manufacturers': Manufacturer.objects.values(),
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
    manufacturer = get_object_or_404(Manufacturer, id=id)
    if request.method == 'POST':
        manufacturer_form = ManufacturerForm(data=request.POST, instance=manufacturer)
        if manufacturer_form.is_valid():
            manufacturer_form.save()
            name = manufacturer_form.cleaned_data["name"]

            # Create a warning notification to be displayed on the page
            messages.warning(request, f"Manufacturer {name} has been updated!")
            return redirect('manage_manufacturer')
    else:
        manufacturer_form = ManufacturerForm(instance=manufacturer)
    context = {
        'manufacturer_form': manufacturer_form,
        'manufacturers': Manufacturer.objects.values(),
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
            manufacturer = product_form.cleaned_data["manufacturer"]

            # Create a new object to be inserted in database
            model_product = Product(name=name,
                                    description=description,
                                    price=price,
                                    quantity=quantity,
                                    icon=request.FILES["icon"],
                                    category=category,
                                    manufacturer=manufacturer)

            # Save the object in database with the above values
            model_product.save()

            # Get list of categories from database
            context['products'] = Product.objects.values()

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
            'products': Product.objects.values(),
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
            product_form.save()
            name = product_form.cleaned_data["name"]

            # Create a warning notification to be displayed on the page
            messages.warning(request, f"Product {name} has been updated!")
            return redirect('manage_product')
    else:
        product_form = ProductForm(instance=product)
    context = {
        'product_form': product_form,
        'products': Product.objects.values(),
    }
    return render(request, 'cosmetics/management/product.html', context)


def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    context = {
        'product': product,
    }
    return render(request, 'cosmetics/product_detail.html', context)

