from django.db import models
from django.utils import timezone

# Create your models here.
class User(models.Model):

    fname=models.CharField(max_length=100)
    lname=models.CharField(max_length=100)
    email=models.CharField(max_length=100)
    mobile=models.CharField(max_length=100)
    password=models.CharField(max_length=100)
    cpassword=models.CharField(max_length=100)
    status=models.CharField(max_length=100,default="inactive")
    usertype=models.CharField(max_length=100,default="user")
    user_image=models.ImageField(upload_to='user_image/',default="")

    def __str__(self):
        return self.fname+" "+self.lname

class Book(models.Model):
    CHOICES = (
        ("python",'python'),
        ("java",'java'),
        ("php",'php'),
        ("c",'c'),
    )
    book_category=models.CharField(max_length=100,choices=CHOICES,default="")
    book_name=models.CharField(max_length=100)
    book_author=models.CharField(max_length=100)
    book_price=models.CharField(max_length=100)
    book_desc=models.TextField()
    book_image=models.ImageField(upload_to='books/',default="")
    book_stock=models.CharField(max_length=100,default="Available")
    user=models.ForeignKey(User,on_delete=models.CASCADE,default="",null=True,blank=True)

    def __str__(self):
        return self.user.fname +" -- "+ self.book_name

class Contact(models.Model):

    name=models.CharField(max_length=100)
    email=models.CharField(max_length=100)
    mobile=models.CharField(max_length=100)
    feedback=models.TextField()

    def __str__(self):
          return self.name

class Wishlist(models.Model):

    user=models.ForeignKey(User,on_delete=models.CASCADE)
    book=models.ForeignKey(Book,on_delete=models.CASCADE)
    added_date=models.DateField(default=timezone.now)

    def __str__(self):

        return self.user.fname+" - "+self.book.book_name

class Cart(models.Model):

    user=models.ForeignKey(User,on_delete=models.CASCADE)
    book=models.ForeignKey(Book,on_delete=models.CASCADE)
    added_date=models.DateField(default=timezone.now)
    total_price=models.IntegerField(default='0')
    total_qty=models.IntegerField()
    
   
    def __str__(self):

        return self.user.fname+" - "+self.book.book_name
