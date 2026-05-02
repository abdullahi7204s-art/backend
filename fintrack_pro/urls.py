from django.contrib import admin
from django.urls import path
from dashboard.views import register_user, login_view, add_expense, get_expenses, reset

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', register_user),
    path('login/', login_view),
    path('expenses/add/', add_expense),
    path('expenses/<int:user_id>/', get_expenses),
    path('reset/', reset),
]
