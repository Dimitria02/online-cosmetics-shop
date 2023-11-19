from django import forms
from crispy_forms.layout import Field, HTML, MultiField
from crispy_forms.helper import FormHelper, Layout
from .models import Category, Manufacturer, Product, Client


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
        fields = ['name', 'description', 'price', 'quantity', 'icon', 'category', 'manufacturer']

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
        Field('manufacturer', css_class='form-control col-md-5'),
    )

