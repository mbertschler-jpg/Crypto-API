from rest_framework import serializers

class CryptoDataSerializer(serializers.Serializer):
    index = serializers.CharField()
    name = serializers.CharField()
    ticker = serializers.CharField()
    #price = serializers.CharField()
    #change_24h = serializers.CharField()
    market_cap = serializers.CharField()
    #volume_24h = serializers.CharField()
    #circulating_supply = serializers.CharField()