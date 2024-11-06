# models.py
from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name



class Rule(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    description = models.TextField()
    rule_number = models.CharField(max_length=20, null=True, blank=True)
    is_applied = models.BooleanField(default=False)
    

    def __str__(self):
        return f"{self.name} - {self.rule_number}" if self.rule_number else self.name
