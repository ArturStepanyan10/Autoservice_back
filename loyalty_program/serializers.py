from rest_framework import serializers

from loyalty_program.models import LoyaltyProfile, BonusTransaction


class LoyaltyProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoyaltyProfile
        fields = ['id', 'user', 'bonus_points']


class BonusTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = BonusTransaction
        fields = ['id', 'user', 'service', 'points', 'timestamp']
