from django.shortcuts import render,redirect
from .models import *
from django.core.mail import send_mail
import random
from django.conf import settings
from datetime import datetime


# Create your views here.
def index(request):
    return render(request,'index.html')

def contact(request):

    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        mobile = request.POST['mobile']
        feedback = request.POST['feedback']

        Contact.objects.create(name=name,email=email,mobile=mobile,feedback=feedback)
        msg = "Contact Saved Successfully"
        contacts=Contact.objects.all().order_by('-id')[:10]
        return render(request,'contact.html',{'msg':msg,'contacts':contacts})
    
    else:
        contacts=Contact.objects.all().order_by('-id')
        return render(request,'contact.html',{'contacts':contacts})

def signup(request):
    if request.method=='POST':
        f=request.POST['fname']
        l=request.POST['lname']
        e=request.POST['email']
        m=request.POST['mobile']
        p=request.POST['password']
        cp=request.POST['cpassword']
        ut=request.POST['usertype']
        ui=request.FILES['user_image']

        try:
            user=User.objects.get(email=e)
            if user:
                msg="Email id already registered"
                return render(request,'signup.html',{'msg':msg,'f':f,'l':l,'m':m})
            
        except:
            if p==cp:
                User.objects.create(fname=f,lname=l,email=e,mobile=m,password=p,
                                    cpassword=cp,usertype=ut,user_image=ui)
                rec=[e,]
                subject="OTP for Successful Registration"
                otp=random.randint(100000,999999)
                message="Your OTP for registration is"+ str(otp)
                email_from= settings.EMAIL_HOST_USER
                send_mail(subject,message,email_from,rec)
                return render(request,'otp.html',{'email':e,'otp':otp})

            else:
                msg="Password & Confirm Password Does Not Matched"
                return render(request,'signup.html',{'msg':msg})
    
    else:
        return render(request,'signup.html')

def login(request):

    if request.method=='POST':
        email=request.POST['email']
        password=request.POST['password']
        usertype=request.POST['usertype']
        
        try:
            user=User.objects.get(email=email,password=password)
            if usertype=="user":
                try:
                    user=User.objects.get(email=email,password=password,usertype=usertype)
                    request.session['email']=user.email
                    request.session['fname']=user.fname
                    wishlists=Wishlist.objects.filter(user=user)
                    request.session['total_wishlist']=len(wishlists)
                    carts=Cart.objects.filter(user=user)
                    request.session['total_cart']=len(carts)
                    request.session['user_image']=user.user_image.url
                    return render(request,'index.html')
                except:
                    msg="Please Select Proper User Type"
                    return render(request,'login.html',{'msg':msg})               
            elif usertype == "seller":
                try:
                    user=User.objects.get(email=email,password=password,usertype=usertype)
                    request.session['email']=user.email
                    request.session['fname']=user.fname
                    return render(request,'seller_index.html')
                except:
                    msg="Please Select Proper User Type"
                    return render(request,'login.html',{'msg':msg})

        except:
            msg="Email or Password Is Incorrect"
            return render(request,'login.html',{'msg':msg})
    
    else:
        return render(request,'login.html')

def validate_otp(request):
    
    myvar=""
    email=request.POST['email']
    otp=request.POST['otp']
    uotp=request.POST['uotp']

    try:
        myvar=request.POST['myvar']

    except:
        pass
        
    if otp==uotp and myvar=="forgot_password":
        return render(request,'enter_new_password.html',{'email':email})
    
    elif otp==uotp:
        try:
            user=User.objects.get(email=email)
            user.status="active"
            user.save()
            msg="Sign Up Successfull"
            return render(request,'login.html',{'msg':msg})
        
        except:
            pass
            
    
    else:
        msg="Entered OTP is Not Correct"
        return render(request,'otp.html',{'msg':msg,'email':email,'otp':otp})

def logout(request):
    try:
        del request.session['fname']
        del request.session['email']
        return render(request,'login.html')
    
    except:
        return render(request,'login.html')

def forgot_password(request):

    if request.method=="POST":
        email=request.POST['email']

        try:
            user=User.objects.get(email=email)
            rec=[email,]
            subject="OTP for Forgot Password"
            otp=random.randint(100000,999999)
            message="Your OTP for Forgot Password is"+ str(otp)
            email_from= settings.EMAIL_HOST_USER
            send_mail(subject,message,email_from,rec)
            myvar="forgot_password"
            return render(request,'otp.html',{'email':email,'otp':otp,'myvar':myvar})
        
        except:
            msg="Email Id Does Not Exists"
            return render(request,'enter_email.html',{'msg':msg})
    
    else:
        return render(request,'enter_email.html')

def update_password(request):

    email=request.POST['email']
    npassword=request.POST['npassword']
    cnpassword=request.POST['cnpassword']

    if npassword==cnpassword:
        user=User.objects.get(email=email)
        user.password=npassword
        user.cpassword=cnpassword
        user.save()
        msg="Password is Upadated Successfully"
        return render(request,'login.html',{'msg':msg})
    
    else:
        msg="New password and Confirm new password Does not Matched"
        return render(request,'enter_new_password.html',{'msg':msg,'email':email})

def change_password(request):
    if request.method=="POST":
        old_password=request.POST['old_password']
        new_password=request.POST['new_password']
        cnew_password=request.POST['cnew_password']

        user=User.objects.get(email=request.session['email'])
        if old_password==user.password:
            if new_password==cnew_password:
                user.password=new_password
                user.cpassword=cnew_password
                user.save()
                return redirect('logout')
            
            else:
                msg="New password and Confirm New Pasword Does Not Matched"
                return render(request,'change_password.html',{'msg':msg})
    
        else:
            msg="Old Pasword Does Not Matched"
            return render(request,'change_password.html',{'msg':msg})
    
    else:
        return render(request,'change_password.html')

def seller_index(request):
    return render(request,'seller_index.html')

def add_book(request):
    
    if request.method== "POST":

        user=User.objects.get(email=request.session['email'])
        bc = request.POST['book_category']
        bn = request.POST['book_name']
        bp = request.POST['book_price']
        ba = request.POST['book_author']
        bd = request.POST['book_desc']
        bi = request.FILES['book_image']

        books=Book.objects.filter(user=user)
        for b in books:
            if b.book_name.lower() == bn.lower():
                msg="Book Already Exists"
                return render(request,'add_book.html',{'msg':msg})
                
        else:
            Book.objects.create(book_category=bc,book_name=bn,book_author=ba,book_price=bp,book_desc=bd,book_image=bi,user=user)
            msg="Book Added Successfully"
            return render(request,'add_book.html',{'msg':msg})

    else:
        return render(request,'add_book.html')

def view_book(request):
    user=User.objects.get(email=request.session['email'])
    books=Book.objects.filter(user=user)

    return render(request,'view_book.html',{'books':books})

def book_detail(request,pk):
    book=Book.objects.get(pk=pk)
    return render(request,'book_detail.html',{'book':book})

def stock_availability(request,pk):
    
    book=Book.objects.get(pk=pk)
    if book.book_stock == "Available":
        book.book_stock = "Unavailable"
        book.save()
    else:
        book.book_stock = "Available"
        book.save()
    return redirect('book_detail',pk)

def book_delete(request,pk):
    book=Book.objects.get(pk=pk)
    book.delete()
    return redirect('view_book')

def book_edit(request,pk):
    if request.method == "POST":
        book=Book.objects.get(pk=pk)
        book.book_name = request.POST['book_name']
        book.book_price = request.POST['book_price']
        book.book_author = request.POST['book_author']
        book.book_desc = request.POST['book_desc']
        
        try:
            if request.FILES['book_image']:
                book.book_image=request.FILES['book_image']
                book.save()
                return redirect('view_book')

        except:
            book.save()
            return redirect('view_book')

    else:
        book=Book.objects.get(pk=pk)
        return render(request,'book_edit.html',{'book':book})

def unavailable_books(request):

    user=User.objects.get(email=request.session['email'])
    books=Book.objects.filter(book_stock="Unavailable",user=user)
    print(books)
    return render(request,'unavailable_books.html',{'books':books})

def available_books(request):

    user=User.objects.get(email=request.session['email'])
    books=Book.objects.filter(book_stock="Available",user=user)
    print(books)
    return render(request,'available_books.html',{'books':books})

def search_book(request):
    user=User.objects.get(email=request.session['email'])
    search=request.POST['search']
    books=Book.objects.filter(book_name__contains=search,user=user)
    return render(request,'search_book.html',{'books':books})

def show_book(request,bn):
    books=Book.objects.filter(book_name__contains=bn)
    return render(request,'show_book.html',{'books':books})

def user_book_detail(request,pk):
    flag=False
    flag1=False
    book=Book.objects.get(pk=pk)
    user=User.objects.get(email=request.session['email'])
    wishlists=Wishlist.objects.filter(user=user,book=book)
    carts=Cart.objects.filter(user=user,book=book)
    for i in wishlists:
        if i.book.pk==book.pk:
            flag=True
            break
    for i in carts:
        if i.book.pk==book.pk:
            flag1=True
            break
    return render(request,'user_book_detail.html',{'book':book,'flag':flag,'flag1':flag1})

def add_to_wishlist(request,pk):
    
    book=Book.objects.get(pk=pk)
    user=User.objects.get(email=request.session['email'])
    Wishlist.objects.create(user=user,book=book)
    return redirect('mywishlist')

def remove_from_wishlist(request,pk):
    
    book=Book.objects.get(pk=pk)
    user=User.objects.get(email=request.session['email'])
    wishlist=Wishlist.objects.get(user=user,book=book)
    wishlist.delete()
    return redirect('mywishlist')
     
def mywishlist(request):

    user=User.objects.get(email=request.session['email'])
    wishlists=Wishlist.objects.filter(user=user)
    request.session['total_wishlist']=len(wishlists)
    return render(request,'mywishlist.html',{'wishlists':wishlists})

def add_to_cart(request,pk):
    
    book=Book.objects.get(pk=pk)
    user=User.objects.get(email=request.session['email'])
    Cart.objects.create(user=user,book=book,total_price=book.book_price,total_qty=1)
    return redirect('mycart')

def remove_from_cart(request,pk):
    
    book=Book.objects.get(pk=pk)
    user=User.objects.get(email=request.session['email'])
    cart=Cart.objects.get(user=user,book=book)
    cart.delete()
    return redirect('mycart')
    
def mycart(request):

    net_price=0
    user=User.objects.get(email=request.session['email'])
    carts=Cart.objects.filter(user=user)
    for i in carts:
        net_price=net_price+i.total_price
    request.session['total_cart']=len(carts)
    return render(request,'mycart.html',{'carts':carts,'net_price':net_price})

def move_to_cart(request,pk):

    book=Book.objects.get(pk=pk)
    user=User.objects.get(email=request.session['email'])
    Cart.objects.create(user=user,book=book,total_price=book.book_price,total_qty=1)
    wishlist=Wishlist.objects.get(user=user,book=book)
    wishlist.delete()
    wishlists=Wishlist.objects.filter(user=user)
    request.session['total_wishlist']=len(wishlists)
    return redirect('mycart')

def move_to_wishlist(request,pk):

    book=Book.objects.get(pk=pk)
    user=User.objects.get(email=request.session['email'])
    Wishlist.objects.create(user=user,book=book)
    cart=Cart.objects.get(user=user,book=book)
    cart.delete()
    carts=Cart.objects.filter(user=user)
    request.session['total_cart']=len(carts)
    return redirect('mywishlist')

def profile(request):
    if request.method == "POST":
        user = User.objects.get(email=request.session['email'])
        user.fname = request.POST['fname']
        user.lname = request.POST['lname']
        user.email = request.POST['email']
        user.mobile = request.POST['mobile']

        try:
            if request.FILES['user_image']:
                user.user_image = request.FILES['user_image']
                user.save()
                request.session['user_image']=user.user_image.url
                return redirect('index')
         
        except:
            user.save()
            return redirect('index')

    else:          
        user = user=User.objects.get(email=request.session['email'])
        return render(request,'profile.html',{'user':user})

def update_price(request):
    price=request.POST['price']
    qty=request.POST['qty']
    pk=request.POST['pk']

    cart=Cart.objects.get(pk=pk)
    total_price=int(price)*int(qty)
    cart.total_price=total_price
    cart.total_qty=qty
    cart.save()
    return redirect('mycart')