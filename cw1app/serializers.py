from rest_framework import serializers
from django.contrib.auth.models import User
from cw1app.models import Professor, Module, ModuleInstance, Rating
from django.db.models import Avg

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "email", "password"]

class ProfessorSerializer(serializers.ModelSerializer):
    avgRating = serializers.SerializerMethodField

    class Meta:
        model = Professor
        fields = ["code", "name", "avgRating"]

    # calculate average rating across all taught modules dynamically
    def calcAvgRating(self, obj):
        avgRating = Rating.objects.filter(professor_id=obj).aggregate(Avg("score"))["rating_avg"]
        if avgRating:
            return round(avgRating)
        else:
            return -1

class ModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = ["code", "name"]

class ModuleInstanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModuleInstance
        fields = ["code", "year", "semester", "leaders"]

class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ["user", "professor", "module", "year", "semester", "score"]
    
    def create(self, data):
        request = self.context.get("request")
        data["user"] = request.user
        return Rating.objects.create(**data)