from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register_view, name="register"),
    path("query/railway/<str:q>", views.query_railway, name="queryrailway"),
    path("query/busstop/<str:q>", views.query_busstop, name="querybusstop"),
    path("train", views.train, name="train"),
    path("bus", views.bus, name="bus"),
    path("review_bus", views.review_bus, name="review_bus"),
    path("review_train", views.review_train, name="review_train"),
    path("train/ticket/book", views.book_train, name="book_train"),
    path("bus/ticket/book", views.book_bus, name="book_bus"),
    path("ticket/payment", views.payment, name="payment"),
    path('ticket/api/<str:booktype>/<str:ref>', views.ticket_data, name="ticketdata"),
    path('ticket/print',views.get_ticket, name="getticket"),
    path('bookings', views.bookings, name="bookings"),
    path('ticket/cancel', views.cancel_ticket, name="cancelticket"),
    path('ticket/resume', views.resume_booking, name="resumebooking"),
    path('contact', views.contact, name="contact"),
    path('privacy-policy', views.privacy_policy, name="privacypolicy"),
    path('terms-and-conditions', views.terms_and_conditions, name="termsandconditions"),
    path('about-us', views.about_us, name="aboutus"),
]
