from rest_framework.serializers import ModelSerializer

from .models import Test, Question


class QuestionSerializer(ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'


class TestSerializer(ModelSerializer):
    

    class Meta:
        model = Test
        fields = '__all__'




