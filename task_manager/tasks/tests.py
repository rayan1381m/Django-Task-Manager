from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Task

class TaskViewsTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='password123')
        self.client.login(username='testuser', password='password123')
        self.task = Task.objects.create(title='Test Task', description='This is a test task', owner=self.user)

    def test_task_list_create_view(self):
        response = self.client.get(reverse('tasks:list_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/task_list_create.html')

    def test_task_detail_view(self):
        response = self.client.get(reverse('tasks:detail', kwargs={'pk': self.task.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/task_detail.html')
        self.assertEqual(response.context['task'], self.task)

    def test_task_update_view(self):
        response = self.client.get(reverse('tasks:edit', kwargs={'pk': self.task.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/task_form.html')

    def test_task_delete_view(self):
        response = self.client.get(reverse('tasks:delete', kwargs={'pk': self.task.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/task_confirm_delete.html')

    def test_task_creation(self):
        response = self.client.post(reverse('tasks:list_create'), {'title': 'New Task', 'description': 'Description of new task'})
        self.assertEqual(response.status_code, 302)  
        self.assertTrue(Task.objects.filter(title='New Task').exists())

    def test_task_deletion(self):
        response = self.client.post(reverse('tasks:delete', kwargs={'pk': self.task.pk}))
        self.assertEqual(response.status_code, 302)  
        self.assertFalse(Task.objects.filter(pk=self.task.pk).exists())

