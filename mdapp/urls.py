from django.urls import path 
from . import views
from django.contrib.auth.decorators import login_required

app_name = 'mdapp'

urlpatterns = [
    # path('', views.index, name='index'),
    path('', login_required(views.List.as_view()), name='index'),
    path('create/', login_required(views.CreateFile.as_view()), name='create'),
    path('files/<str:pk>', login_required(views.Detail.as_view()), name='ditail'),
    path('files/<str:pk>/update', login_required(views.UpdateFile.as_view()), name='update'),
    path('files/<str:pk>/delete', login_required(views.Delet.as_view()), name='delete'),
    path('files/<str:pk>/pdf', login_required(views.get_pdf_bytedeta), name='pdf')
]
