from django.urls import path 
from . import views

app_name = 'mdapp'

urlpatterns = [
    # path('', views.index, name='index'),
    path('', views.List.as_view(), name='index'),
    path('files/<int:pk>', views.Detail.as_view(), name='ditail'),
    path('files/<int:pk>/update', views.UpdateFile.as_view(), name='update'),
    path('create/', views.CreateFile.as_view(), name='create'),
    # path('create/<int:pk>', views.CreateFile.as_view(), name='update')
]
