from django.shortcuts import render
from rest_framework.decorators import api_view,permission_classes
from .models import Product,ProductImages,Review
from rest_framework.response import Response
from .serializers import ProductSerializers,ProductImageSerializers
from django.shortcuts import get_object_or_404
from .filters import ProductFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework import status
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from django.db.models import Avg


# Create your views here.

@api_view(['GET'])
def get_products(request):
    filterset=ProductFilter(request.GET,queryset=Product.objects.all().order_by('id'))
    #products=Product.objects.all()
    count=filterset.qs.count()
    # paggination
    resperpage=10
    paginator=PageNumberPagination()
    paginator.page_size=resperpage
    queryset=paginator.paginate_queryset(filterset.qs,request)

    serializer=ProductSerializers(queryset,many=True)
    #print(products)
    return Response(
        {"count":count,
            "Products":serializer.data
            })

@api_view(['GET'])
def get_product(request,pk):
    product=get_object_or_404(Product,id=pk)
    serializer=ProductSerializers(product,many=False)
    return Response({"Product": serializer.data})



@api_view(['POST'])
@permission_classes([IsAuthenticated,IsAdminUser])
def new_product(request):
    data=request.data
    serializer=ProductSerializers(data=data)
    if serializer.is_valid():
        product=Product.objects.create(**data,user=request.user)
        #serializer=ProductSerializers(product,many=False)
        product = Product.objects.create(**data, user=request.user)
        res = ProductSerializers(product, many=False)
        return Response({ "product": res.data })
    else:
        return Response(serializer.errors)
    

@api_view(['POST'])
@permission_classes([IsAuthenticated,IsAdminUser])
def uplodeProduct_images(request):
    data=request.data
    files=request.FILES.getlist('images')
    print('files',files)
    images=[]
    for f in files:
        image=ProductImages.objects.create(product=Product(data['product']),Image=f)
        images.append(image)
    serializer=ProductImageSerializers(images,many=True)
    return Response(serializer.data)


@api_view(['PUT'])
@permission_classes([IsAuthenticated,IsAdminUser])
def update_product(request,pk):
    product=get_object_or_404(Product,id=pk)
    # check if the user is same
    if product.user!=request.user:
        return Response({"Error":'you cannot update this product'},status=status.HTTP_403_FORBIDDEN)
    product.Name=request.data['Name']
    product.Description=request.data['Description']
    product.Price=request.data['Price']
    product.Brand=request.data['Brand']
    product.Category=request.data['Category']
    product.Stock=request.data['Stock']
    product.Rating=request.data['Rating']
    product.save()
    return Response({"Message":'Product Updated SuccesFully'})


@api_view(['DELETE'])
@permission_classes([IsAuthenticated,IsAdminUser])
def delete_product(request,pk):
    product=get_object_or_404(Product,id=pk)
    # check if the user is same
    if product.user!=request.user:
        return Response({"Error":'you cannot update this product'},status=status.HTTP_403_FORBIDDEN)
    args={"product":pk}
    images=ProductImages.objects.filter(**args)
    for i in images:
        i.delete()
    product.delete()
    return Response({"Message":'Product Deleted SuccesFully'},status=status.HTTP_200_OK)



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_review(request,pk):
    user=request.user
    product=get_object_or_404(Product,id=pk)
    data=request.data
    reviews=product.review.filter(User=user)# --

    if data['rating']<=0 or data['rating']>5:
        return Response({"Error":'Please Select Rating between 1 to 5'},status=status.HTTP_400_BAD_REQUEST)
    elif reviews.exists():
        new_review={
            'rating':data['rating'],
            'comment':data['comment']
        }
        reviews.update(**new_review)
        rating=product.review.aggregate(avg_ratings=Avg('rating'))
        product.Rating=rating['avg_ratings']
        product.save()
        return Response({"detail":'Review Updated'})
    else:
        Review.objects.create(
            User=user, #--
            product=product,
            rating=data['rating'],
            comment=data['comment']
        )
        rating=product.review.aggregate(avg_ratings=Avg('rating'))
        product.Rating=rating['avg_ratings']
        product.save()
        return Response({"detail":'Review posted'})
    

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_review(request,pk):
    user=request.user
    product=get_object_or_404(Product,id=pk)
    reviews=product.review.filter(User=user)

    if reviews.exists():
        reviews.delete()
        rating=product.review.aggregate(avg_ratings=Avg('rating'))
        if rating['avg_ratings'] is None:
            rating['avg_ratings']=0
        product.Rating=rating['avg_ratings']
        product.save()
        return Response({"detail":'Review deleted'})
    else:
        return Response({"Error":'review not found'},status=status.HTTP_404_NOT_FOUND)



