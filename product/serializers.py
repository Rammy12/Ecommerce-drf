from rest_framework import serializers
from .models import Product,ProductImages,Review

class ReviewSerializers(serializers.ModelSerializer):
    class Meta:
        model=Review
        fields="__all__"


class ProductImageSerializers(serializers.ModelSerializer):
    class Meta:
        model=ProductImages
        fields="__all__"

class ProductSerializers(serializers.ModelSerializer):
    images=ProductImageSerializers(many=True,required=False)
    review=serializers.SerializerMethodField(method_name='get_reviews',read_only=True)
    class Meta:
        model=Product
        fields=('id','Name','Description','Price','Brand','Category','Rating','Stock','review','images')
        extra_kwargs={
            "Name":{"required": True,"allow_blank":False},
            "Description":{"required": True,"allow_blank":False},
            "Brand":{"required": True,"allow_blank":False},
            "Category":{"required": True,"allow_blank":False}
        }
    def get_reviews(self,obj):
        reviews=obj.review.all()
        serializer=ReviewSerializers(reviews,many=True)
        return serializer.data





