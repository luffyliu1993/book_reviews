from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$',views.index),
    url(r'^login$',views.login_check),
    url(r'^register$',views.register),
    url(r'^books$',views.show_books),
    url(r'^books/add$',views.add_book),
    url(r'^logout$',views.logout),
    url(r'^receive_book_info$',views.process_book),
    url(r'^books/(?P<book_id>\d+?)',views.show_one_book),
    url(r'^add_review/(?P<book_id>\d+?)$',views.add_review)
]
