from django.urls import path 
from . import views

app_name = 'mdapp'

urlpatterns = [
    # path('', views.index, name='index'),
    path('', views.List.as_view(), name='index'),
    path('create/', views.CreateFile.as_view(), name='create'),
    path('files/<int:pk>', views.Detail.as_view(), name='ditail'),
    path('files/<int:pk>/update', views.UpdateFile.as_view(), name='update'),
    path('files/<int:pk>/delete', views.Delet.as_view(), name='delete'),
    path('files/<int:pk>/pdf', views.get_pdf_bytedeta, name='pdf')
]
