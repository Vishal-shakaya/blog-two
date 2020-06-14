
from django.urls import path , include 
from comment import views 
app_name = 'Comment'

urlpatterns =[
path('add-comment/<int:pk>/', views.CreateComment.as_view(), name='add_comment'),
]