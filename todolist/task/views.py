from django.shortcuts import render,redirect,HttpResponse,HttpResponseRedirect,get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth  import authenticate,login as auth_login,logout 
from django.contrib import messages
from .models import Todo
from .forms import *

# Create your views here.
def signup(request):
    if request.method == 'POST':
        user_name = request.POST.get('user_name')
        email = request.POST.get('email')
        password1 = request.POST.get('password')
        password2 = request.POST.get('confirm_password')

        print(user_name, email, password1, password2)

        if password1 == password2:
            if User.objects.filter(username=user_name).exists():
                messages.error(request,'User Already Exists!!')
                return redirect('signup')
            else:
                my_data = User.objects.create_user(user_name,email,password1)
                auth_login(request,my_data)
                messages.success(request,'Registration Successful.')
                # my_data.save()
                return redirect('signup')
        else:
            messages.error(request,'Password do not match.')
            return redirect('signup')
            # return HttpResponse("Password doesn't match")
    return render(request, 'signup.html')


def login(request):
    if request.method == 'POST':
        user_name = request.POST.get('user_name')
        password = request.POST.get('password')
        print(user_name, password)
        user = authenticate(request, username=user_name, password=password)

        if user is not None:
            auth_login(request, user)
            messages.success(request,'You are logged in.')
            return redirect('base')
        else:
            # return HttpResponseRedirect('User or Password is Incorrect.')
           messages.error(request,"User or Password is Incorrect.")

    return render(request, 'login.html')

def base(request):
    return render(request, "base.html")

def todo_list(request):
    todos = Todo.objects.all()
    return render(request,'base.html',{'todos':todos})

def create_todo(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        Todo.objects.create(title=title,description=description)
        messages.success(request,'Task Added Successfully')
    return redirect('/base')

def edit_todo(request,todo_id):
    # todo_id = request.GET.get('id')
    print(todo_id)

    todo = get_object_or_404(Todo, id=todo_id)
    
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=todo)
        if form.is_valid():
            form.save()
            return redirect('/base')
    else:
        form = TaskForm(instance=todo)
    
    context = {'form': form}
    return render(request, 'edit.html', context)


def delete_todo(request,todo_id):
    todo = Todo.objects.get(id=todo_id)
    todo.delete()
    messages.error(request,'Task deleted Successfully')
    return redirect('base')
