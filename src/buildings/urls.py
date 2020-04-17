from django.urls import path
from . import views

# urlpatterns = [
#     path('', views.list, name='list')
# ]

from .views import BuildingListView, BuildingSearchDateView

app_name = 'buildings'

urlpatterns = [
    path('<str:date>', BuildingListView.as_view(), name='building-list'),
    path('', BuildingSearchDateView.as_view(), name='building-search-date'),
    path('search/', views.search, name='search'),
    path('addbuilding/', views.addbuilding, name='addbuilding'),
    path('addroom/', views.addroom, name='addroom'),
    path('addinterval/', views.addinterval, name='addinterval'),
    path('addfeature/', views.addfeature, name='addfeature'),
    path('thanksb/', views.thanksb, name='thanksb'),
    path('thanksr/', views.thanksr, name='thanksr'),
    path('thanksi/', views.thanksi, name='thanksi'),
    path('thanksf/', views.thanksf, name='thanksf'),
    path('editroom/<int:pk>/', views.editroom, name='editroom'),
]