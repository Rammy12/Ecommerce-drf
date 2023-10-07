from rest_framework import serializers
from .models import OrderItem,Order



class OrderItemSerializers(serializers.ModelSerializer):
    class Meta:
        model=OrderItem
        fields="__all__"



class OrderSerializers(serializers.ModelSerializer):
    orderItems=serializers.SerializerMethodField(method_name='get_order_item',read_only=True)
    class Meta:
        model=Order
        fields="__all__"
    
    def get_order_item(self,obj):
        order_item=obj.orderitems.all()
        serializer=OrderItemSerializers(order_item,many=True)
        return serializer.data