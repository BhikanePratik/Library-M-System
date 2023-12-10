from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views



urlpatterns = [

# Shared URL's
 path('', views.login_form, name='home'),
 path('login/', views.loginView, name='login'),
 path('logout/', views.logoutView, name='logout'),
 path('regform/', views.register_form, name='regform'),
 path('register/', views.registerView, name='register'),




    # Admin URL's
 path('dashboard/', views.dashboard, name='dashboard'),

 path('asearch/', views.asearch, name='asearch'),
 path('adbookk/<int:pk>', views.ADeleteBookk.as_view(), name='adbookk'),

 path('create_user_form/', views.create_user_form, name='create_user_form'),
 path('create_use/', views.create_user, name='create_user'),
 path('aluser/', views.ListUserView.as_view(), name='aluser'),
 path('alvuser/<int:pk>', views.ALViewUser.as_view(), name='alvuser'),
 path('aeuser/<int:pk>', views.AEditUser.as_view(), name='aeuser'),
 path('aduser/<int:pk>', views.ADeleteUser.as_view(), name='aduser'),

 path('acchat/', views.ACreateChat.as_view(), name='acchat'),
 path('alchat/', views.AListChat.as_view(), name='alchat'),

 path('adminadd_book/', views.adminaddbook_form, name='adminaddbook_form'),
 path('aabook/', views.aaddbook, name='aabook'), 
 path('adminbook_list/', views.adminbookListView.as_view(), name='adminbooklist'),
 path('amanagebook/', views.adminManageBook.as_view(), name='amanagebook'),
 path('ambook/', views.adminManageBook.as_view(), name='ambook'),
 path('avbook/<int:pk>', views.AViewBook.as_view(), name='avbook'),
 path('aebook/<int:pk>', views.AEditView.as_view(), name='aebook'),
 path('adbook/<int:pk>', views.ADeleteBook.as_view(), name='adbook'),





    # Librarian URL's
 path('librarian/', views.librarian, name='librarian'),

 path('lsearch/', views.lsearch, name='lsearch'),
 path('ldbook/<int:pk>', views.LDeleteBook.as_view(), name='ldbook'),

 path('lcchat/', views.LCreateChat.as_view(), name='lcchat'),
 path('llchat/', views.LListChat.as_view(), name='llchat'),
 
 path('labook/', views.Labaddbook, name='labook'), 
 path('add_book/', views.Labaddbook_form, name='addbook_form'),
 path('book_list/', views.LabbookListView.as_view(), name='booklist'),

 path('managebook/', views.LabManageBook.as_view(), name='managebook'),
 path('lvbook/<int:pk>', views.LabViewBook.as_view(), name='lvbook'),
 path('lebook/<int:pk>', views.LabEditView.as_view(), name='lebook'),
 path('labdbook/<int:pk>', views.LabDeleteView.as_view(), name='labdbook'),

 path('viewissuedbook/', views.viewissuedbook_view,name="viewissuedbook"),
 path('issuebook/', views.issuebook_view, name="issuebook"),

    # Student URL's
 path('student/', views.student, name='student'), 
 path("studenthome/", views.studenthome, name="studenthome"),
 path('scchat/', views.SCreateChat.as_view(), name='scchat'),
 path('slchat/', views.SListChat.as_view(), name='slchat'),
 path("view_issued_book/", views.view_issued_book, name="view_issued_book"),
 path('viewissuedbookbystudent/', views.viewissuedbookbystudent,name="viewissuedbookbystudent"),
 





]
