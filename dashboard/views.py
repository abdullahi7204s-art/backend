import json
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from .models import DBExpense

@csrf_exempt
def register_user(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            username = data.get("username")
            password = data.get("password")
            if not username or not password:
                return JsonResponse({"detail": "Username and password required"}, status=400)
            if User.objects.filter(username=username).exists():
                return JsonResponse({"detail": "Username already taken"}, status=400)
            user = User.objects.create_user(username=username, password=password)
            return JsonResponse({"id": user.id, "username": user.username}, status=201)
        except Exception as e:
            return JsonResponse({"detail": str(e)}, status=400)
    return JsonResponse({"error": "POST only"}, status=405)

@csrf_exempt
def login_view(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user = authenticate(username=data.get("username"), password=data.get("password"))
            if user is not None:
                return JsonResponse({"id": user.id, "username": user.username})
            return JsonResponse({"error": "Invalid credentials"}, status=401)
        except:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
    return JsonResponse({"error": "POST only"}, status=405)

@csrf_exempt
def add_expense(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            expense = DBExpense.objects.create(
                user_id=data.get("user_id"),
                amount=float(data.get("amount")),
                category=data.get("category"),
                description=data.get("description", "")
            )
            return JsonResponse({
                "id": expense.id,
                "amount": expense.amount,
                "category": expense.category,
                "description": expense.description,
                "date_created": expense.date_created
            }, status=201)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

def get_expenses(request, user_id):
    try:
        # Expenses are retrieved and sorted by Nairobi time as configured
        expenses = DBExpense.objects.filter(user_id=user_id).order_by('-date_created').values()
        return JsonResponse(list(expenses), safe=False)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@csrf_exempt
def reset(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user_id = data.get("user_id")
            # Deletes all records associated with the specific user_id
            DBExpense.objects.filter(user_id=user_id).delete()
            return JsonResponse({"message": "All data reset successfully"}, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "POST only"}, status=405)
