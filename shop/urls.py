from . import views
from django.urls import path, include
from register import views as v

urlpatterns = [
    path("", views.index, name='ShopHome'),
    path("about/", views.about, name='AboutUs'),
    path("contact/", views.contact, name='ContactUs'),
    path("tracker/", views.tracker, name='TrackingStatus'),
    path("search/", views.search, name='Search'),
    path("products/<int:proid>", views.productView, name='ProductView'),
    path("checkout/", views.checkout, name='Checkout'),
    path("paymentstatus/", views.handlerequest, name='HandleRequest'),
    path("register/", v.register, name='Register'),
    path("menfashion/", views.men, name='MenFashion'),
    path("womenfashion/", views.women, name='MenFashion'),
    path("", include("django.contrib.auth.urls")),
]
