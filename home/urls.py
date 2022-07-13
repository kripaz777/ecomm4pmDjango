from django.urls import path
from .views import *

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('details/<slug>', ProductDetailView.as_view(), name='details'),
	path('add_review', review, name='add_review')
]
