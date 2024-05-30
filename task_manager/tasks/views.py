from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.db.models import Q
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer
from .models import Task
from django.contrib.auth.models import User
from .forms import TaskCreateForm, TaskUpdateForm, searchForm

class RegisterView(CreateView):
    model = User
    template_name = 'registration/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    success_message = "User added"

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        for field in form.fields.values():
            field.help_text = None
        return form

class TaskBaseView(LoginRequiredMixin, APIView):
    renderer_classes = [TemplateHTMLRenderer]

class TaskListCreateView(TaskBaseView):
    template_name = 'tasks/task_list_create.html'

    def get(self, request):
        form_task = TaskCreateForm()
        form_search = searchForm(request.GET)
        search = form_search.data.get('search')
        if search:
            tasks = Task.objects.filter(Q(title__icontains=search) | Q(description__icontains=search))
            form_search = searchForm(initial={'search': search})
            messages.success(request, f'Search results for: {search}')
        else:
            tasks = Task.objects.all()
        return render(request, 'tasks/task_list_create.html', {'tasks': tasks, 'form_task': form_task, 'form_search': form_search})

    def post(self, request):
        form_task = TaskCreateForm(request.POST)
        if form_task.is_valid():
            task = form_task.save(commit=False)
            task.owner = request.user
            task.save()
            messages.success(request, 'Task added')
            return redirect(reverse_lazy('tasks:list_create'))
        return render(request, 'tasks/task_list_create.html', {'form_task': form_task})

class TaskDetailView(TaskBaseView):
    template_name = 'tasks/task_detail.html'

    def get(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        return render(request, 'tasks/task_detail.html', {'task': task})

class TaskDeleteView(TaskBaseView):
    template_name = 'tasks/task_confirm_delete.html'

    def get(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        if task.owner != request.user:
            return render(request, 'tasks/error.html', {'error': 'This task does not belong to you'})
        return render(request, 'tasks/task_confirm_delete.html', {'task': task})

    def post(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        if task.owner == request.user:
            task.delete()
            messages.success(request, 'Task deleted')
        else:
            messages.error(request, 'You are not authorized to delete this task!')
        return redirect(reverse_lazy('tasks:list_create'))

class TaskUpdateView(TaskBaseView):
    template_name = 'tasks/task_form.html'

    def get(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        if task.owner != request.user:
            return render(request, 'tasks/error.html', {'error': 'Only the owner can edit'})

        creation_date = task.created_at.strftime('%Y-%m-%d')
        form = TaskUpdateForm(instance=task)
        return render(request, 'tasks/task_form.html', {'form': form, 'creation_date': creation_date})

    def post(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        if task.owner != request.user:
            return render(request, 'tasks/error.html', {'error': 'Only the owner can edit'})

        form = TaskUpdateForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, 'Task updated')
            return redirect(reverse_lazy('tasks:list_create'))
        return render(request, 'tasks/task_form.html', {'form': form})
