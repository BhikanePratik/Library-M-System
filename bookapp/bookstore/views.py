from datetime import date
from django import forms
from django.db.models import Q
from typing import Any
from django.db.models.query import QuerySet
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views import generic
from bootstrap_modal_forms.mixins import PassRequestMixin
from .models import IssuedItem, User, Book, Chat
from django.contrib import messages
from django.db.models import Sum
from django.views.generic import CreateView, DetailView, DeleteView, UpdateView, ListView
from .forms import BookForm ,ChatForm ,UserForm, IssuedBookForm
from . import models
import operator
import itertools
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import authenticate, logout
from django.contrib import auth, messages
from django.contrib.auth.hashers import make_password
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.utils import timezone
import django.utils.datetime_safe

	# Create your views here.

	# Shared Views              
def register_form(request):
    return render(request, 'bookstore/register.html')

def registerView (request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirmpassword = request.POST['confirmpassword']
      
        if password == confirmpassword:
            password = make_password(password)
            a = User(username = username, email = email, password = password)
            a.save()
            messages.success(request, 'Account created successfully')
            return redirect('home')
        else:
            messages.error(request,'Password do not match.')
            return redirect('regform')
        return render(request, 'bookstore/register.html')
    
def login_form(request):
	return render(request, 'bookstore/login.html')



def loginView(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username = username, password = password)
        if user is not None and user.is_active:
            auth.login(request, user)
            if user.is_admin or user.is_superuser:  
                return redirect('dashboard')
            elif user.is_librarian:
                return redirect('librarian')
            else:
                return redirect('studenthome')
        else:
            messages.info(request, "Invalid username or password")
            return redirect('home')
    
def logoutView(request):
	logout(request)
	return redirect('home')



       #Librarian views
       ################################################################################################
def librarian(request):
	book = Book.objects.all().count()
	user = User.objects.all().count()

	context = {'book':book, 'user':user}

	return render(request, 'librarian/home.html', context)

@login_required
def lsearch(request):
    query = request.GET['query']
    print(type(query))


    #data = query.split()
    data = query
    print(len(data))
    if( len(data) == 0):
        return redirect('student')
    else:
                a = data

                # Searching for It
                qs5 =models.Book.objects.filter(title__iexact=a).distinct()
                qs6 =models.Book.objects.filter(title__exact=a).distinct()

                qs7 =models.Book.objects.all().filter(title__contains=a)
                qs8 =models.Book.objects.select_related().filter(title__contains=a).distinct()
                qs9 =models.Book.objects.filter(title__startswith=a).distinct()
                qs10 =models.Book.objects.filter(title__endswith=a).distinct()
                qs11 =models.Book.objects.filter(title__istartswith=a).distinct()
                qs12 =models.Book.objects.all().filter(title__icontains=a)
                qs13 =models.Book.objects.filter(title__iendswith=a).distinct()

                files = itertools.chain(qs5, qs6, qs7, qs8, qs9, qs10, qs11, qs12, qs13)

                res = []
                for i in files:
                    if i not in res:
                        res.append(i)


                # word variable will be shown in html when user click on search button
                word="Searched Result :"
                print("Result")

                print(res)
                files = res




                page = request.GET.get('page', 1)
                paginator = Paginator(files, 10)
                try:
                    files = paginator.page(page)
                except PageNotAnInteger:
                    files = paginator.page(1)
                except EmptyPage:
                    files = paginator.page(paginator.num_pages)
   


                if files:
                    return render(request,'librarian/result.html',{'files':files,'word':word})
                return render(request,'librarian/result.html',{'files':files,'word':word})
    

class LCreateChat(LoginRequiredMixin, CreateView):
	form_class = ChatForm
	model = Chat
	template_name = 'librarian/chat_form.html'
	success_url = reverse_lazy('llchat')
      
	def form_valid(self, form):
		self.object = form.save(commit=False)
		self.object.user = self.request.user
		self.object.save()
		return super().form_valid(form)




class LListChat(LoginRequiredMixin, ListView):
	model = Chat
	template_name = 'librarian/chat_list.html'

	def get_queryset(self):
		return Chat.objects.filter(posted_at__lt=timezone.now()).order_by('posted_at')

class LDeleteBook(LoginRequiredMixin,DeleteView):
	model = Book
	template_name = 'librarian/confirm_delete2.html'
	success_url = reverse_lazy('librarian')
	success_message = 'Data was dele successfully'
    
@login_required
def Labaddbook_form(request):
	return render(request, 'librarian/add_book.html')

@login_required
def Labaddbook(request):
    if request.method == 'POST':
        title = request.POST['title']
        author = request.POST['author']
        subject = request.POST['subject']
        cover = request.FILES['cover']
        pdf = request.FILES['pdf']
        current_user = request.user
        user_id = current_user.id
        username = current_user.username
        
        a = Book(title=title, author=author, 
                 subject=subject, cover=cover, pdf=pdf, user_id=user_id)
        a.save()
        messages.success(request, 'Book was uploaded successfully')
        return redirect('booklist')
    else:
        messages.error(request, 'Book was not uploaded successfully')
        return redirect('booklist')
    
class LabbookListView(LoginRequiredMixin,ListView):
	model = Book
	template_name = 'librarian/book_list.html'
	context_object_name = 'books'
	paginate_by = 3

	def get_queryset(self):
		return Book.objects.order_by('-id')
      
 
class LabManageBook(LoginRequiredMixin,ListView):
	model = Book
	template_name = 'librarian/manage_books.html'
	context_object_name = 'books'
	paginate_by = 3

	def get_queryset(self):
		return Book.objects.order_by('-id')
      
class LabViewBook(LoginRequiredMixin,DetailView):
	model = Book
	template_name = 'librarian/book_detail.html'
      
class LabEditView(LoginRequiredMixin,UpdateView):
	model = Book
	form_class = BookForm
	template_name = 'librarian/edit_book.html'
	success_url = reverse_lazy('managebook')
	success_message = 'Data was updated successfully'
      
class LabDeleteView(LoginRequiredMixin,DeleteView):
	model = Book
	template_name = 'librarian/confirm_delete.html'
	success_url = reverse_lazy('managebook')
	success_message = 'Data was deleted successfully'
      
        
def viewissuedbook_view(request):
    issuedbooks=models.IssuedItem.objects.all()
    print('hello')
    li=[]
    for ib in issuedbooks:
        issdate=str(ib.issue_date.day)+'-'+str(ib.issue_date.month)+'-'+str(ib.issue_date.year)
        expdate=str(ib.expiry_date.day)+'-'+str(ib.expiry_date.month)+'-'+str(ib.expiry_date.year)
        #fine calculation
        days=(date.today()-ib.issue_date)
        print(date.today())
        d=days.days
        fine=0
        if d>15:
            day=d-15
            fine=day*10


        books=list(models.Book.objects.filter(id=ib.book_id))
        students=list(models.User.objects.filter(id=ib.user_id))
        i=0
        print('hi') 
        for l in books:
            t=(students[i].username,books[i].title,books[i].author,issdate,expdate,fine)
            i=i+1
            li.append(t)

    return render(request,'librarian/viewissuedbook.html',{'li':li})


@login_required
def  issuebook_view(request):
    form=IssuedBookForm()
    if request.method=='POST':   
        #now this form have data from html
        form=IssuedBookForm(request.POST)
        if form.is_valid():
            # obj=models.IssuedItem()
            # obj.user_id=request.POST.get('username')
            # obj.book_id=request.POST.get('title')
            issued_item = form.save()
            return render(request,'librarian/bookissued.html')
    return render(request,'librarian/issuebook.html',{'form':form})

    
     #Admin views


def dashboard(request):
	book = Book.objects.all().count()
	user = User.objects.all().count()

	context = {'book':book, 'user':user}

	return render(request, 'dashboard/home.html', context)




@login_required
def asearch(request):
    query = request.GET['query']
    print(type(query))


    #data = query.split()
    data = query
    print(len(data))
    if( len(data) == 0):
        return redirect('dashborad')
    else:
                a = data

                # Searching for It
                qs5 =models.Book.objects.filter(title__iexact=a).distinct()
                qs6 =models.Book.objects.filter(title__exact=a).distinct()

                qs7 =models.Book.objects.all().filter(title__contains=a)
                qs8 =models.Book.objects.select_related().filter(title__contains=a).distinct()
                qs9 =models.Book.objects.filter(title__startswith=a).distinct()
                qs10 =models.Book.objects.filter(title__endswith=a).distinct()
                qs11 =models.Book.objects.filter(title__istartswith=a).distinct()
                qs12 =models.Book.objects.all().filter(title__icontains=a)
                qs13 =models.Book.objects.filter(title__iendswith=a).distinct()




                files = itertools.chain(qs5, qs6, qs7, qs8, qs9, qs10, qs11, qs12, qs13)

                res = []
                for i in files:
                    if i not in res:
                        res.append(i)


                # word variable will be shown in html when user click on search button
                word="Searched Result :"
                print("Result")

                print(res)
                files = res




                page = request.GET.get('page', 1)
                paginator = Paginator(files, 10)
                try:
                    files = paginator.page(page)
                except PageNotAnInteger:
                    files = paginator.page(1)
                except EmptyPage:
                    files = paginator.page(paginator.num_pages)
   


                if files:
                    return render(request,'dashboard/result.html',{'files':files,'word':word})
                return render(request,'dashboard/result.html',{'files':files,'word':word})




@login_required
def adminaddbook_form(request):
	return render(request, 'dashboard/add_book.html')

@login_required
def aaddbook(request):
    if request.method == 'POST':
        title = request.POST['title']
        author = request.POST['author']
        subject = request.POST['subject']
        cover = request.FILES['cover']
        pdf = request.FILES['pdf']
        current_user = request.user
        user_id = current_user.id
        username = current_user.username
        
        a = Book(title=title, author=author, 
                 subject=subject, cover=cover, pdf=pdf, user_id=user_id)
        a.save()
        messages.success(request, 'Book was uploaded successfully')
        return redirect('adminbooklist')
    else:
        messages.error(request, 'Book was not uploaded successfully')
        return redirect('adminbooklist')

class adminbookListView(LoginRequiredMixin,ListView):
	model = Book
	template_name = 'dashboard/book_list.html'
	context_object_name = 'books'
	paginate_by = 3

	def get_queryset(self):
		return Book.objects.order_by('-id')
      
 
class adminManageBook(LoginRequiredMixin,ListView):
	model = Book
	template_name = 'dashboard/manage_books.html'
	context_object_name = 'books'
	paginate_by = 3

	def get_queryset(self):
		return Book.objects.order_by('-id')
      
class AViewBook(LoginRequiredMixin,DetailView):
	model = Book
	template_name = 'dashboard/book_detail.html'
      
class AEditView(LoginRequiredMixin,UpdateView):
	model = Book
	form_class = BookForm
	template_name = 'dashboard/edit_book.html'
	success_url = reverse_lazy('ambook')
	success_message = 'Data was updated successfully'
      
class ADeleteBook(LoginRequiredMixin,DeleteView):
	model = Book
	template_name = 'dashboard/confirm_delete.html'
	success_url = reverse_lazy('dashboard')
	success_message = 'Data was delete successfully'

class ADeleteBookk(LoginRequiredMixin,DeleteView):
	model = Book
	template_name = 'dashboard/confirm_delete2.html'
	success_url = reverse_lazy('ambook')
	success_message = 'Data was delete successfully'


	
def create_user_form(request):
    choice = ['1', '0', 'Student', 'Admin', 'Librarian']
    choice = {'choice': choice}

    return render(request, 'dashboard/add_user.html', choice)

def create_user(request):
    choice = ['1', '0', 'Student', 'Admin', 'Librarian']
    choice = {'choice': choice}
    if request.method == 'POST':
            first_name=request.POST['first_name']
            last_name=request.POST['last_name']
            username=request.POST['username']
            userType=request.POST['userType']
            email=request.POST['email']
            password=request.POST['password']
            password = make_password(password)
            print("User Type",userType)
            print(userType)
            if userType == "Student":
                a = User(first_name=first_name, last_name=last_name, username=username, email=email, password=password, is_student=True)
                a.save()
                messages.success(request, 'Member was created successfully!')
                return redirect('aluser')
            elif userType == "Admin":
                a = User(first_name=first_name, last_name=last_name, username=username, email=email, password=password, is_admin=True)
                a.save()
                messages.success(request, 'Member was created successfully!')
                return redirect('aluser')
            elif userType == "Librarian":
                a = User(first_name=first_name, last_name=last_name, username=username, email=email, password=password, is_librarian=True)
                a.save()
                messages.success(request, 'Member was created successfully!')
                return redirect('aluser')    
            else:
                messages.success(request, 'Member was not created')
                return redirect('create_user_form')
    else:
        return redirect('create_user_form')


class ACreateChat(LoginRequiredMixin, CreateView):
	form_class = ChatForm
	model = Chat
	template_name = 'dashboard/chat_form.html'
	success_url = reverse_lazy('alchat')


	def form_valid(self, form):
		self.object = form.save(commit=False)
		self.object.user = self.request.user
		self.object.save()
		return super().form_valid(form)

class AListChat(LoginRequiredMixin, ListView):
	model = Chat
	template_name = 'dashboard/chat_list.html'

	def get_queryset(self):
		return Chat.objects.filter(posted_at__lt=timezone.now()).order_by('posted_at')
      


class AEditUser(SuccessMessageMixin, UpdateView): 
    model = User
    form_class = UserForm
    template_name = 'dashboard/edit_user.html'
    success_url = reverse_lazy('aluser')
    success_message = "Data successfully updated"

class ListUserView(generic.ListView):
    model = User
    template_name = 'dashboard/list_users.html'
    context_object_name = 'users'
    paginate_by = 4

    def get_queryset(self):
        return User.objects.order_by('-id')
    
class ALViewUser(DetailView):
    model = User
    template_name='dashboard/user_detail.html'

class ADeleteUser(SuccessMessageMixin, DeleteView):
    model = User
    template_name='dashboard/confirm_delete3.html'
    success_url = reverse_lazy('aluser')
    success_message = "Data successfully deleted"



# Student views
def student(request):
        return render(request, 'student/base.html')

def studenthome(request):
        return render(request, 'student/home.html')

class SCreateChat(LoginRequiredMixin, CreateView):
	form_class = ChatForm
	model = Chat
	template_name = 'student/chat_form.html'
	success_url = reverse_lazy('slchat')


	def form_valid(self, form):
		self.object = form.save(commit=False)
		self.object.user = self.request.user
		self.object.save()
		return super().form_valid(form)

class SListChat(LoginRequiredMixin, ListView):
	model = Chat
	template_name = 'student/chat_list.html'

	def get_queryset(self):
		return Chat.objects.filter(posted_at__lt=timezone.now()).order_by('posted_at')
      

def view_issued_book(request):
    issue_item = issue_item.objects.all()
    details = []
    for i in issue_item:
        days = (date.today()-i.issued_date)
        d=days.days
        fine=0
        if d>14:
            day=d-14
            fine=day*5
        books = list(models.Book.objects.filter(id=i.book_id))
        users = list(models.User.objects.filter(user=i.user_id))
        i=0
        for l in books:
            t=(users[i].user,users[i].user_id,books[i].title,issue_item[0].issued_date,issue_item[0].expiry_date,fine)
            i=i+1
            details.append(t)
    return render(request, "student/issue.html", {'issue_item':issue_item, 'details':details})


@login_required
def viewissuedbookbystudent(request):
    student = models.User.objects.filter(id=request.user.id).first()
    # issuedbooks = models.IssuedItem.objects.filter(user=student)
    # issuedbook=models.IssuedItem.objects.filter(id=student[0].user.id)
    issuedbooks = models.IssuedItem.objects.filter(user_id=student.id).all()

    li1=[]

    li2=[]
    for ib in issuedbooks:
        books=models.Book.objects.filter(id=ib.book_id)
        for book in books:
            # t=(request.user,student[0].username,book.title,book.author)
            t = (book.title, book.author, book.subject)

            li1.append(t)
        issdate=str(ib.issue_date.day)+'-'+str(ib.issue_date.month)+'-'+str(ib.issue_date.year)
        expdate=str(ib.expiry_date.day)+'-'+str(ib.expiry_date.month)+'-'+str(ib.expiry_date.year)
        #fine calculation
        days=(date.today()-ib.issue_date)
        print(date.today())
        d=days.days
        fine=0
        if d>15:
            day=d-15
            fine=day*10
        t=(issdate,expdate,fine)
        li2.append(t)

    return render(request,'student/viewissuedbookbystudent.html',{'li1':li1,'li2':li2})


