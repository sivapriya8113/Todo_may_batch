from typing import Any
from django.db.models.query import QuerySet
from django.http import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView,FormView, ListView , DetailView,UpdateView,DeleteView
from  django.contrib.auth.forms import UserCreationForm
from .models import Tasks
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.

class CustomLoginView(LoginView):
    template_name = 'login.html'
    fields = '__all__'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return reverse_lazy('task')


class RegisterView(FormView):
    template_name = 'register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('task')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request,user)
        return super(RegisterView,self).form_valid(form)

    def get(self,*args,**kwargs):
        if self.request.user.is_authenticated:
            return redirect('task')
        return super(RegisterView,self).get(*args,**kwargs)



  
class TaskList(LoginRequiredMixin,ListView):
    model = Tasks
    context_object_name = 'task'
    template_name = 'tasklist.html'
    
    def get_queryset(self):
       return Tasks.objects.filter(user=self.request.user)


class TaskCreate(LoginRequiredMixin,CreateView):
    model = Tasks
    fields = ['task','description','completed']
    success_url = reverse_lazy('task')
    template_name = 'taskcreate.html'
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreate,self).form_valid(form)
    
    
  
        

class TaskDetailView(DetailView):
    model = Tasks
    template_name = 'taskdetails.html'
        

class TaskUpdate(UpdateView):
    model = Tasks
    fields = ['task','description','completed']
    success_url = reverse_lazy('task')
    template_name = 'taskcreate.html'
    
class TaskDelete(DeleteView):
    model = Tasks
    success_url = reverse_lazy('task')
    template_name = 'taskdelete.html'
   
