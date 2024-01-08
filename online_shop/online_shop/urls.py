"""
URL configuration for online_shop project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth
from client import views as client_views
from cosmetics import views as cosmetics_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', cosmetics_views.home, name='home'),
    path('login/', client_views.client_login, name='client_login'),
    path('logout/', auth.LogoutView.as_view(template_name='cosmetics/home.html'), name='logout'),
    path('signup/', client_views.client_signup, name='client_signup'),
    path('profile/', cosmetics_views.user_profile, name='user_profile'),
    path('categories/', cosmetics_views.categories, name='categories'),
    path('categories/<int:id>/<str:sort>/', cosmetics_views.products_from_category, name='products_from_category'),
    path('subcategories/<int:id>/', cosmetics_views.products_from_subcategory, name='products_from_subcategory'),
    path('manufacturers/<int:id>/', cosmetics_views.products_from_manufacturer, name='products_from_manufacturer'),
    path('cart/', cosmetics_views.view_cart, name='view_cart'),
    path('add/<int:id>/', cosmetics_views.add_to_cart, name='add_to_cart'),
    path('remove/<int:id>/', cosmetics_views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', cosmetics_views.view_checkout, name='view_checkout'),
    path('management/', cosmetics_views.management, name='management'),
    path('management/category', cosmetics_views.manage_category, name='manage_category'),
    path('management/category/delete/<int:id>', cosmetics_views.delete_category, name='delete_category'),
    path('management/category/edit/<int:id>', cosmetics_views.update_category, name='update_category'),
    path('management/subcategory', cosmetics_views.manage_subcategory, name='manage_subcategory'),
    path('management/subcategory/delete/<int:id>', cosmetics_views.delete_subcategory, name='delete_subcategory'),
    path('management/subcategory/edit/<int:id>', cosmetics_views.update_subcategory, name='update_subcategory'),
    path('management/order', cosmetics_views.manage_order, name='manage_order'),
    path('management/order/delete/<int:id>', cosmetics_views.delete_order, name='delete_order'),
    path('management/order/edit/<int:id>', cosmetics_views.update_order, name='update_order'),
    path('management/product', cosmetics_views.manage_product, name='manage_product'),
    path('management/product/delete/<int:id>', cosmetics_views.delete_product, name='delete_product'),
    path('management/product/edit/<int:id>', cosmetics_views.update_product, name='update_product'),
    path('management/manufacturer', cosmetics_views.manage_manufacturer, name='manage_manufacturer'),
    path('management/manufacturer/delete/<int:id>', cosmetics_views.delete_manufacturer, name='delete_manufacturer'),
    path('management/manufacturer/edit/<int:id>', cosmetics_views.update_manufacturer, name='update_manufacturer'),
    path('product/<int:id>', cosmetics_views.product_detail, name='product_detail'),
    path('simple_queries/', cosmetics_views.simple_queries, name='simple_queries'),
    path('simple_dynamic_queries/', cosmetics_views.simple_dynamic_queries, name='simple_dynamic_queries'),
    path('complex_queries/', cosmetics_views.complex_queries, name='complex_queries'),
    path('statistics/', cosmetics_views.statistics, name='statistics'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
