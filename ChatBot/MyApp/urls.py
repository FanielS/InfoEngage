from turtle import home
from . import views
from django.urls import path

urlpatterns = [
    path("", views.home, name='home'),
    path("/services", views.services, name='services'),
    path("/about", views.about, name='about'),
    path("/contact", views.contact, name='contact'),
    path("/faq", views.faq, name='faq'),
    path("/pdf_chat", views.pdf_chat, name='pdf_chat'),
    path("/youtube_summarizer", views.youtube_summarizer, name='youtube_summarizer'),
    path('chat_pdf/', views.chat_pdf, name='chat_pdf'),
    path('summarize', views.summarize, name='summarize'),
    path('ask_question/', views.ask_question_view, name='ask_question'),
    path('create_assistant/', views.create_assistant, name='create_assistant'),
]