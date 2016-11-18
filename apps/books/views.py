from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User,Book,Author,Review

# Create your views here.
def index(request):
    return render(request,'books/index.html')

def login_check(request):
    login_messages = User.userManager.login(request.session,str(request.POST['email']),str(request.POST['password']))
    if login_messages[0]:
        return redirect('/books')
    for message in login_messages[1]['errors']:
        messages.add_message(request,messages.ERROR,message,extra_tags='login')
    return redirect('/')

def register(request):
    register_messages = User.userManager.register_check(request.session,str(request.POST['fname']),str(request.POST['lname']),\
            str(request.POST['email']),str(request.POST['password']),str(request.POST['conf_pw']))
    if register_messages[0]:
        return redirect('/books')
    for message in register_messages[1]['errors']:
        messages.add_message(request,messages.ERROR,message,extra_tags='register')
    return redirect('/')

def add_book(request):
    return render(request,'books/add_book.html')

def logout(request):
    request.session.pop('id')
    return redirect('/')

def process_book(request):
    selected_author_name = str(request.POST['selected_author_name'])
    entered_author_name = str(request.POST['entered_author_name'])
    if len(entered_author_name) == 0:
        if selected_author_name == 'None':
            author_name = ''
        else:
            author_name = selected_author_name
    else:
        author_name = entered_author_name
    book = Book.bookManager.add_book(request.session,str(request.POST['book_title']),author_name,str(request.POST['review']),int(request.POST['rating']))
    return redirect('/books/'+str(book[1].id))

def show_one_book(request,book_id):
    book = Book.bookManager.get(id=book_id)
    reviews = Review.objects.filter(book__id=book_id)
    data = {
        'book':book,
        'reviews':reviews
    }
    return render(request,'books/show_one_book.html',data)

def show_books(request):
    user = User.userManager.get(id=request.session['id'])
    reviews = Review.objects.all().order_by('-id')[:3]
    books = Book.bookManager.all()
    data = {
        'user':user,
        'reviews':reviews,
        'books':books
    }
    return render(request,'books/books.html',data)

def add_review(request,book_id):
    user = User.userManager.get(id=request.session['id'])
    book = Book.bookManager.get(id=book_id)
    Review.objects.create(review=str(request.POST['review']),rating=int(request.POST['rating']),user=user,book=book)
    return redirect('/books/'+book_id)
