from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Vendor, PurchaseOrder
from .serializers import VendorSerializer, PurchaseOrderSerializer,VendorPerformanceSerializer
from django.utils import timezone
from rest_framework.decorators import api_view, authentication_classes
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import AllowAny
from rest_framework import status
from .serializers import UserSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken


@api_view(['POST'])
def signup(request):
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'error': 'Only POST requests are allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    try:
        refresh_token = request.data['refresh_token']
        token = RefreshToken(refresh_token)
        token.blacklist()
        return Response({"message": "Logout successful"}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def obtain_jwt_token(request):
    if request.method == 'POST':
        serializer = TokenObtainPairSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response({'error': 'Only POST requests are allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def vendors_list(request):
    if request.method == 'GET':
        vendors = Vendor.objects.all()
        serializer = VendorSerializer(vendors, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = VendorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

# GET /api/vendors/{vendor_id}/: Retrieve a specific vendor's details
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def retrieve_vendor(request, vendor_id):
    if request.method == 'GET':
        vendor = get_object_or_404(Vendor, pk=vendor_id)
        serializer = VendorSerializer(vendor)
        return Response(serializer.data)


# PUT /api/vendors/{vendor_id}/: Update a vendor's details
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_vendor(request, vendor_id):
    vendor = get_object_or_404(Vendor, pk=vendor_id)
    if request.method == 'PUT':
        serializer = VendorSerializer(vendor, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)


# DELETE /api/vendors/{vendor_id}/: Delete a vendor
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_vendor(request, vendor_id):
    vendor = get_object_or_404(Vendor, pk=vendor_id)
    if request.method == 'DELETE':
        vendor.delete()
        return Response({'message': 'Vendor deleted successfully'}, status=204)


# ------------------------- Purchase order logic----------------------------

@api_view(['POST', 'GET'])
@permission_classes([IsAuthenticated])
def purchase_order(request):
    if request.method == 'POST':
        serializer = PurchaseOrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    elif request.method == 'GET':
        vendor_id = request.GET.get('vendor_id')  # Optional vendor filter
        if vendor_id:
            purchase_orders = PurchaseOrder.objects.filter(vendor_id=vendor_id)
        else:
            purchase_orders = PurchaseOrder.objects.all()
        serializer = PurchaseOrderSerializer(purchase_orders, many=True)
        return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def retrieve_purchase_order(request, po_id):
    if request.method == 'GET':
        purchase_order = get_object_or_404(PurchaseOrder, pk=po_id)
        serializer = PurchaseOrderSerializer(purchase_order)
        return Response(serializer.data)

# PUT /api/purchase_orders/{po_id}/: Update a purchase order
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_purchase_order(request, po_id):
    purchase_order = get_object_or_404(PurchaseOrder, pk=po_id)
    if request.method == 'PUT':
        serializer = PurchaseOrderSerializer(purchase_order, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

# DELETE /api/purchase_orders/{po_id}/: Delete a purchase order
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_purchase_order(request, po_id):
    purchase_order = get_object_or_404(PurchaseOrder, pk=po_id)
    if request.method == 'DELETE':
        purchase_order.delete()
        return Response({'message': 'Purchase order deleted successfully'}, status=204)
    

# -----------------------performance matrics--------------------
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def retrieve_vendor_performance(request, vendor_id):
    if request.method == 'GET':
        vendor = Vendor.objects.get(pk=vendor_id)
        vendor.update_performance_metrics()  # Update performance metrics before retrieving
        serializer = VendorPerformanceSerializer(vendor)
        return Response(serializer.data)
    

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def acknowledge_purchase_order(request, po_id):
    purchase_order = get_object_or_404(PurchaseOrder, pk=po_id)
    if request.method == 'POST':
        acknowledgment_date = timezone.now()
        purchase_order.acknowledgment_date = acknowledgment_date
        purchase_order.save()

        # Calculate response time in seconds
        response_time = (acknowledgment_date - purchase_order.issue_date).total_seconds()

        # Update the purchase order's average response time
        purchase_order.vendor.update_response_time(response_time)
        
        return Response({'message': 'Purchase order acknowledged successfully'}, status=200)