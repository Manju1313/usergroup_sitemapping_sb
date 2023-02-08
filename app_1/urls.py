from django.urls import path
from . import views
from .views import *


urlpatterns = [
    path('', views.login_view, name='login_view'),
    path('login/', views.login_view, name='login_view'),
    path('select/', views.select, name='select'),
    path('logout/',views.logout_view, name="logout"),
    path('replace/',views.replace, name="replace"),
    # path('notes', Notes.as_view()),
    # path('<str:pk>', NoteDetail.as_view()),
    path('about/', NewView.as_view()),  
    path('create/', EmployeeCreate.as_view(), name = 'EmployeeCreate'),
    path('retrieve/', EmployeeRetrieve.as_view(), name = 'EmployeeRetrieve'),  
    path('retrieve/<int:pk>', EmployeeDetail.as_view(), name = 'EmployeeDetail'),  
    path('<int:pk>/update/', EmployeeUpdate.as_view(), name = 'EmployeeUpdate'),  
    path('<int:pk>/delete/', EmployeeDelete.as_view(), name = 'EmployeeDelete'),  
    path('signup', signup, name = 'home'),  
    path('form/', activate, name = 'index'),  
    # path('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/',  
    #     activate, name='activate'),  

]

