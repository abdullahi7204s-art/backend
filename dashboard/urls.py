from django.urls import path
from .views import login_view, add_expense, get_expenses, reset

urlpatterns = [
    path("login/", login_view),
    path("expenses/add/", add_expense),
    path("expenses/<int:user_id>/", get_expenses),
    path("reset/", reset),
]
