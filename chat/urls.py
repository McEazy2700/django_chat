from django.urls import path
from .views import MessageGetAndCreateView, MessageDetailView


urlpatterns = [
    path("message/", MessageGetAndCreateView.as_view(), name="message"),
    path("message/<int:pk>/", MessageDetailView.as_view(), name="message_detail"),
]
