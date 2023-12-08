from datetime import date, datetime, timedelta
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User  # Import User from django.contrib.auth
from django.urls import reverse
from django.utils import timezone


class User(AbstractUser):
    is_admin = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)
    is_librarian = models.BooleanField(default=False)

    class Meta:
        swappable = 'AUTH_USER_MODEL'
class Book(models.Model):
    title = models.CharField(max_length=150)
    author = models.CharField(max_length=200)
    quantity = models.IntegerField(default=1)
    subject = models.CharField(max_length=2000)
    book_add_time = models.TimeField(default=timezone.now)
    book_add_date = models.DateField(default=timezone.now)
    pdf = models.FileField(upload_to='bookapp/pdfs/')
    cover = models.ImageField(upload_to='bookapp/covers/', null=True, blank=True)
    user_id = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.title

def expiry():
    return datetime.today() + timedelta(days=14)
class IssuedItem(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    issue_date = models.DateField(default=timezone.now, blank=False)
    expiry_date = models.DateField(default=expiry)
    return_date = models.DateField(blank=True, null=True)

    @property
    def title(self):
        return self.book.title

    @property
    def username(self):
        return self.user.username

    def __str__(self):
        return (
            self.book.title
            + " issued by "
            + self.user.first_name
            + " on "
            + str(self.issue_date)
        )

    def delete(self, *args):
        self.book.pdf.delete()
        self.book.cover.delete()
        super().delete(*args)


class Chat(models.Model):
    user_chat_id = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    posted_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return str(self.message)




























# User = get_user_model()


# class User(AbstractUser):
#     is_admin = models.BooleanField(default=False)
#     is_student = models.BooleanField(default=False)
#     is_librarian = models.BooleanField(default=False)


#     class Meta:
#         swappable = 'AUTH_USER_MODEL'


# class Book(models.Model):
    # title = models.CharField(max_length=150)
    # author = models.CharField(max_length=200)
    # quantity = models.IntegerField(default=1)
    # subject = models.CharField(max_length=2000)
    # book_add_time = models.TimeField(default=timezone.now())
    # book_add_date = models.DateField(default=date.today())
    # pdf = models.FileField(upload_to='bookapp/pdfs/')
    # cover = models.ImageField(upload_to='bookapp/covers/', null=True, blank=True)
    # user_id = models.CharField(max_length=100, null=True, blank=True)

    # def __str__(self):
    #     return self.title

    # IssuedItem model to store issued book details

# def expiry():
#     return datetime.today() + timedelta(days=14)
# class IssuedItem(models.Model):
#     book = models.ForeignKey(Book, on_delete=models.CASCADE)
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     issue_date = models.DateField(default=date.today(), blank=False)
#     expiry_date = models.DateField(default=expiry)
#     return_date = models.DateField(blank=True, null=True)
    
#     # property to get book name
#     @property
#     def title(self):
#         return self.book_id.title
    
#     # property to get author name
#     @property
#     def username(self):
#         return self.user_id.username
    
#     def __str__(self):
#         return (
#             self.book_id.book_name
#             + " issued by "
#             + self.user_id.first_name
#             + " on "
#             + str(self.issue_date)
#         )

#     def delete(self, *args, **kwargs):
#         # You need to use self.book.pdf and self.book.cover to access the FileField of the Book model
#         self.book.pdf.delete()
#         self.book.cover.delete()
#         super().delete(*args, **kwargs)   























# class Chat(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     message = models.TextField()
#     posted_at = models.DateTimeField(auto_now=True, null=True)


#     def __str__(self):
#         return str(self.message)
















