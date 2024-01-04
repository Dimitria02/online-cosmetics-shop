from django import forms
from crispy_forms.layout import Field, HTML, MultiField
from crispy_forms.helper import FormHelper, Layout
from .models import Category, Subcategory, Manufacturer, Product, Order


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'icon']

    helper = FormHelper()
    helper.form_tag = False
    helper.form_class = 'form-group'
    helper.layout = Layout(
        Field('name', css_class='form-control col-md-5'),
        Field('icon', css_class='form-control col-md-5'),
    )


class SimpleDynamicQuery1Form(forms.Form):
    category_name = forms.CharField(label="Category Name")


class SimpleDynamicQuery2Form(forms.Form):
    manufacturer_name = forms.CharField(label="Manufacturer Name")


class SimpleDynamicQuery3Form(forms.Form):
    product_quantity = forms.IntegerField(label="Product Quantity")


class SimpleDynamicQuery4Form(forms.Form):
    start_date = forms.DateField(label="Start Date")
    stop_date = forms.DateField(label="Stop Date")


class SimpleDynamicQuery5Form(forms.Form):
    new_category_name = forms.CharField(label="Category Name")


class SimpleDynamicQuery6Form(forms.Form):
    product_price = forms.IntegerField(label="Product Quantity")


class SimpleDynamicQuery7Form(forms.Form):
    filters = (("AW", "Awaiting"), ("PR", "Processing"), ("FI", "Finalized"))
    status_order = forms.ChoiceField(label="Status Order", choices=filters)


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['status', 'street', 'city', 'country', 'zip_code']

    helper = FormHelper()
    helper.form_tag = False
    helper.form_class = 'form-group'
    helper.layout = Layout(
        Field('status', css_class='form-control col-md-5'),
        Field('street', css_class='form-control col-md-5'),
        Field('city', css_class='form-control col-md-5'),
        Field('country', css_class='form-control col-md-5'),
        Field('zip_code', css_class='form-control col-md-5'),
    )


class ShippingForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['street', 'city', 'country', 'zip_code']

    helper = FormHelper()
    helper.form_tag = False
    helper.form_class = 'form-group'
    helper.layout = Layout(
        Field('street', css_class='form-control col-md-5'),
        Field('city', css_class='form-control col-md-5'),
        Field('country', css_class='form-control col-md-5'),
        Field('zip_code', css_class='form-control col-md-5'),
    )


class SubcategoryForm(forms.ModelForm):
    class Meta:
        model = Subcategory
        fields = ['name', 'category']

    helper = FormHelper()
    helper.form_tag = False
    helper.form_class = 'form-group'
    helper.layout = Layout(
        Field('name', css_class='form-control col-md-5'),
        Field('category', css_class='form-control col-md-5'),
    )


class ManufacturerForm(forms.ModelForm):
    class Meta:
        model = Manufacturer
        fields = ['name']

    helper = FormHelper()
    helper.form_tag = False
    helper.form_class = 'form-group'
    helper.layout = Layout(
        Field('name', css_class='form-control col-md-5'),
    )


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'quantity', 'icon', 'category', 'subcategory', 'manufacturer']

    helper = FormHelper()
    helper.form_tag = False
    helper.form_class = 'form-group'
    helper.layout = Layout(
        Field('name', css_class='form-control col-md-5'),
        Field('description', css_class='form-control col-md-5'),
        Field('price', css_class='form-control col-md-5'),
        Field('quantity', css_class='form-control col-md-5'),
        Field('icon', css_class='form-control col-md-5'),
        Field('category', css_class='form-control col-md-5'),
        Field('subcategory', css_class='form-control col-md-5'),
        Field('manufacturer', css_class='form-control col-md-5'),
    )

