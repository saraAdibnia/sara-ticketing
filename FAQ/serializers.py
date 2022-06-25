from FAQ.models import FrequentlyAskedQuestion
from rest_framework import serializers

class ShowFrequentlyAskedQuestionSerializer(serializers.ModelSerializer):
    class Meta:
            model = FrequentlyAskedQuestion
            fields = "__all__"

class FrequentlyAskedQuestionSerializer(serializers.ModelSerializer):
    class Meta:
            model = FrequentlyAskedQuestion
            fields="__all__"