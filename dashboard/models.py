from django.db import models
from django.utils import timezone

class DBExpense(models.Model):
    user_id = models.IntegerField()
    amount = models.FloatField()
    category = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    date_created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.category}: {self.amount}"
