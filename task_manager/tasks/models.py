from django.db import models
from django.contrib.auth.models import User

status = [
    ('To Do', 'To Do'),
    ('Done', 'Done'),
]

class Task(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)                                 
    title = models.CharField(max_length=100, blank=False)                                 
    description = models.TextField(blank=True)                                                  
    created_at = models.DateTimeField(auto_now_add=True)                                                                              
    status = models.CharField(max_length=15, choices=status, null=False, default='To Do')
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-title']
        