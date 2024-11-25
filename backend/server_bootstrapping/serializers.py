# serializers.py
from rest_framework import serializers
from .models import Category, Rule

class RuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rule
        fields = ['id', 'name', 'category', 'description', 'is_applied', 'rule_number']

class CategorySerializer(serializers.ModelSerializer):
    rules = RuleSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'rules', ]
