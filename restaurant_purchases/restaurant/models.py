from django.db import models


class Ingridient(models.Model):
    name = models.CharField(max_length=64)
    quantity = models.FloatField()
    unit = models.CharField(max_length=64)
    unit_price = models.FloatField()

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

    def __str__(self):
        return self.menu_item.title
