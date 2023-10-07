from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from .models import Order,OrderItem
from product.models import Product
from .serializers import OrderSerializers
from .filters import OrdersFilters
from rest_framework.pagination import PageNumberPagination
import strip
import os
from utils.helper import get_current_host



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_orders(request):
    filterset=OrdersFilters(request.GET,queryset=Order.objects.all().order_by('id'))
    count=filterset.qs.count()
    # pagination
    resperpage=1
    paginator=PageNumberPagination()
    paginator.page_size=resperpage
    queryset=paginator.paginate_queryset(filterset.qs,request)
    serializer=OrderSerializers(queryset,many=True)
    return Response({
        "count":count,
        "resperpage":resperpage,
        "orders":serializer.data})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_order(request,pk):
    orders=get_object_or_404(Order,id=pk)
    serializer=OrderSerializers(orders,many=False)
    return Response({"orders":serializer.data})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def new_order(request):
    user=request.user
    data=request.data
    order_Items=data['orderItems']
    if order_Items and len(order_Items)==0:
        return Response({"error":'No order item please add one order atleast'},status=status.HTTP_400_BAD_REQUEST)
    else:
        #create order

        total_amount=sum(item['price']*item['quantity'] for item in order_Items)
        order=Order.objects.create(
            User=user,
            street=data['street'],
            city=data['city'],
            state=data['state'],
            zip_code=data['zip_code'],
            phone_no=data['phone_no'],
            country=data['country'],
            total_amount=total_amount
        )

        # create order item set order item 
        for i in order_Items:
            product=Product.objects.get(id=i['product'])
            item=OrderItem.objects.create(
                product=product,
                order=order,
                name=product.Name,
                quantity=i['quantity'],
                price=i['price']
            )
            product.Stock-=item.quantity
            product.save()
        
        serializer=OrderSerializers(order,many=False)
        return Response(serializer.data)

@api_view(['PUT'])
@permission_classes([IsAuthenticated,IsAdminUser])
def process_order(request,pk):
    order=get_object_or_404(Order,id=pk)
    order.order_status=request.data['order_status']
    order.save()
    serializer=OrderSerializers(order,many=False)
    return Response({"orders":serializer.data})

# Create your views here.
@api_view(['DELETE'])
@permission_classes([IsAuthenticated,IsAdminUser])
def delete_order(request,pk):
    order=get_object_or_404(Order,id=pk)
    order.delete()
    return Response({"orders":"oder is deleted"})



#strip.api_key=os.environ.get('STRIPE_PRIVATE_KEY')
#YOUR_DOMAIN=get_current_host()


'''@api_view(['POSt'])
@permission_classes([IsAuthenticated])
def create_checkout(request):
    user=request.user
    data=request.data
    order_items=data['orderItems']
    shipping_details={
        'street':data['street'],
        'city':data['city'],
        'state':data['state'],
        'zip_code':data['zip_code'],
        'phone_no':data['phone_no'],
        'country':data['country'],
        'user':user.id
    }
    checkout_order_items=[]
    for item in order_items:
        checkout_order_items.append(
            {
                'price_data':{
                    'currency':'rs',
                    'product_data':{
                        'name':item['name'],
                        'images':item['image'],
                        'metadata':{
                            'product_id':item['product']} 
                    },
                    'unit_amount':item['price']*100
                },
                'quantity':item['quantity']
            }
        )'''
