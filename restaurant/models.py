from django.db import models


class Ingridient(models.Model):
    name = models.CharField(max_length=64)
    quantity = models.FloatField()
    unit = models.CharField(max_length=64)
    unit_price = models.FloatField()
    temporary_field = models.FloatField(default=0.0)

    def __str__(self):
        return self.name


class MenuItem(models.Model):
    title = models.CharField(max_length=64)
    price = models.FloatField()

    def __str__(self):
        return self.title


class RecipeRequirement(models.Model):
    menu_item = models.ForeignKey(MenuItem, related_name='recipe_requirements', on_delete=models.CASCADE)
    ingridient = models.ForeignKey(Ingridient, related_name='recipe_requirements', on_delete=models.CASCADE)
    quantity = models.FloatField()

    def __str__(self):
        return str(self.menu_item.title) + ' ' + str(self.ingridient.name)


class Purchase(models.Model):
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    price = models.FloatField()

    def __str__(self):
        return self.menu_item.title


STATUS_CHOICES = (
    ("FreeTask", "free_task"),
    ("BusyTask", "busy_task"),
    ("ProcessTask", "process_task")
)


class TelegramNotification(models.Model):
    ingredient = models.ForeignKey(Ingridient, on_delete=models.CASCADE)
    status = models.CharField(max_length=32, choices=STATUS_CHOICES, default="free_task")
    datetime = models.DateTimeField(auto_now=True)

STORE_CHOICES = (
    ("NeedBuy", "need_buy"),
    ("WasBuy", "was_buy")
)

class StoreTask(models.Model):
    ingredient = models.ForeignKey(Ingridient, on_delete=models.CASCADE)
    quantity = models.FloatField()
