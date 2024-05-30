from django.urls import path, include
from .views import TaskListCreateView, TaskDetailUpdateDeleteView, api_root

app_name = 'api'
urlpatterns = [
    path('', api_root, name='api_root'),  
    path('tasks/', TaskListCreateView.as_view(), name='task-list-create'),
    path('tasks/<int:pk>/', TaskDetailUpdateDeleteView.as_view(), name='task-detail-update-delete'),
    path('apis/', include('tasks.urls')),  
]
