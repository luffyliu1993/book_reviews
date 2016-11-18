from __future__ import unicode_literals
from django.db import models
import bcrypt, re

# Create your models here.
class UserManager(models.Manager):
    EMAIL_REGEX = r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$'
    def login(self,session,email,password):
        messages = {'errors':[]}
        if len(email) == 0:
            messages['errors'].append('Please enter an email')
        elif not re.match(self.EMAIL_REGEX,email):
            messages['errors'].append('Email is not valid')
        if len(password) == 0:
            messages['errors'].append('Please enter a password')
        if len(messages['errors']) > 0:
            return (False, messages)
        result = self.filter(email=email)
        if len(result) == 0:
            messages['errors'].append('Incorrect email!')
            return (False, messages)
        if not bcrypt.checkpw(str(password),str(result[0].password)):
            messages['errors'].append('Incorrect password!')
            return (False, messages)
        session['id'] = result[0].id
        return (True, messages)

    def register_check(self,session,fname,lname,email,password,conf_pw):
        messages = {'errors':[]}
        if len(fname) < 2:
            messages['errors'].append('First name should be at least 2 characters long')
        elif not str.isalpha(str(fname)):
            messages['errors'].append('Frist name should be letters only')
        if len(lname) < 2:
            messages['errors'].append('Last name should be at least 2 characters long')
        elif not str.isalpha(str(lname)):
            messages['errors'].append('Last name should be letters only')
        if len(email) == 0:
            messages['errors'].append('Email cannot be empty')
        elif not re.match(self.EMAIL_REGEX,email):
            messages['errors'].append('Email is not valid')
        elif len(self.filter(email=email)) > 0:
            messages['errors'].append('The email you entered is used by another account')
        if len(password) < 8:
            messages['errors'].append('Password should have at least 8 characters')
        if len(conf_pw) == 0:
            messages['errors'].append('Please confirm your password')
        elif password != conf_pw:
            messages['errors'].append('Password and confirm password are not match')
        if len(messages['errors']) > 0:
            return (False, messages)
        result = self.create(first_name=fname,last_name=lname,email=email,password=bcrypt.hashpw(str(password),bcrypt.gensalt()))
        #session['id'] = self.all().order_by('-id')[0].id
        session['id'] = result.id
        return (True, messages)

class BookManager(models.Manager):
    def add_book(self,session,book_title,author,review,rating):
        errors = []
        if len(book_title) == 0:
            errors.append('Please enter a book title')
        if len(author) == 0:
            errors.append('Please enter an author')
        if len(review) == 0:
            errors('Please write a review')
        if len(errors) > 0:
            return (False, errors)
        get_author = Author.authorManager.add_author(author)
        book = self.create(title=book_title,author=get_author)
        user = User.userManager.get(id=session['id'])
        Review.objects.create(review=review,rating=rating,user=user,book=book)
        return (True, book)

class AuthorManager(models.Manager):
    def add_author(self,author_name):
        author = self.filter(name=author_name)
        if author:
            return author[0]
        author = self.create(name=author_name)
        return author

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    userManager = UserManager()

class Author(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    authorManager = AuthorManager()

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey('Author',on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    bookManager = BookManager()

class Review(models.Model):
    review = models.TextField()
    rating = models.IntegerField()
    user = models.ForeignKey('User',on_delete=models.CASCADE,related_name='review_user')
    book = models.ForeignKey('Book',on_delete=models.CASCADE,related_name='review_book')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
