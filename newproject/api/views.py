from rest_framework.views import APIView  # Import APIView cho class-based views
from rest_framework.response import Response
from rest_framework import status
from .serializer import UserSerializer, RegisterSerializer, LoginSerializer, ProductSerializer, CartOrderSerializer, CartOrderDetailSerializer, PaymentSerializer, CartOrderItemSerializer  # Sửa lại tên file nếu cần
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model 
from rest_framework.permissions import IsAuthenticated
from .models import *
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny

# newproject/api/views.py
User = get_user_model()

class RegisterView(APIView):
    def post(self, request):
        # Khởi tạo serializer với dữ liệu từ request
        serializer = RegisterSerializer(data=request.data)
        
        # Kiểm tra dữ liệu có hợp lệ không
        if serializer.is_valid():
            # Nếu hợp lệ, lưu thông tin người dùng
            serializer.save()
            return Response({"message": "Đăng ký thành công!"}, status=status.HTTP_201_CREATED)
        
        # Trả về lỗi nếu dữ liệu không hợp lệ
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        
        # Xác thực người dùng
        user = authenticate(username=username, password=password)
        if user is not None:
            # Tạo JWT token cho người dùng
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)

            return Response(
                {
                    "access": access_token,  # Trả về token
                    "user_id": user.id,  # Trả về user.id
                    "refresh": str(refresh),
                },
                status=status.HTTP_200_OK,
            )
        else:
            return Response({"error": "Tên đăng nhập hoặc mật khẩu không đúng"}, status=status.HTTP_400_BAD_REQUEST)

    
class UserListView(APIView):
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class UserDetailView(APIView):
    def get(self, request, pk):
        try:
            user = User.objects.get(pk=pk)  # Lấy người dùng theo pk
            serializer = UserSerializer(user)  # Serialize thông tin người dùng
            return Response(serializer.data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"error": "Người dùng không tồn tại."}, status=status.HTTP_404_NOT_FOUND)
        
# View sản phẩm:
from rest_framework import viewsets
from .models import Product

class ProductViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]
    def get_queryset(self):
        # Bạn có thể lọc hoặc truy vấn các sản phẩm dựa trên một số tiêu chí, nếu cần.
        return Product.objects.all()
# CartOrder:

class CartOrderViewSet(viewsets.ModelViewSet):
    queryset = CartOrder.objects.all()
    serializer_class = CartOrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CartOrder.objects.filter(user=self.request.user, status='pending')

    def perform_create(self, serializer):
        user = self.request.user
        cart_order = serializer.save(user=user, status='pending', total_price=0)

        # Tính toán lại tổng giá sau khi thêm mục giỏ hàng
        cart_order.total_price = cart_order.items.aggregate(Sum('price'))['price__sum'] or 0
        cart_order.save()  # Lưu lại giỏ hàng với tổng giá đã tính toán

        return cart_order


#CartOrderDetail:

class CartOrderDetailViewSet(viewsets.ModelViewSet):
    queryset = CartOrder.objects.all()
    serializer_class = CartOrderDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        order_id = self.kwargs['pk']  # Lấy ID giỏ hàng từ URL
        return CartOrder.objects.filter(id=order_id, user=self.request.user) # Lọc theo người dùng và ID đơn hàng
#AddProduct: 

class AddProductToCartView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user  # Lấy user đã đăng nhập từ request (đảm bảo người dùng đã được xác thực)
        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity', 1)  # Số lượng mặc định là 1

        try:
            # Kiểm tra xem sản phẩm có tồn tại không
            product = Product.objects.get(id=product_id)

            # Kiểm tra xem giỏ hàng đã tồn tại chưa
            cart_order = CartOrder.objects.filter(user=user, status='pending').first()

            if not cart_order:
                # Nếu không có giỏ hàng, tạo một giỏ hàng mới
                cart_order = CartOrder.objects.create(user=user, total_price=0, status='pending')

            # Kiểm tra số lượng hợp lệ
            if quantity <= 0:
                return Response({"error": "Số lượng phải lớn hơn 0."}, status=status.HTTP_400_BAD_REQUEST)

            if quantity > product.quantity:  # Kiểm tra nếu số lượng yêu cầu vượt quá tồn kho
                return Response({"error": f"Số lượng sản phẩm vượt quá tồn kho ({product.quantity} còn lại)."}, status=status.HTTP_400_BAD_REQUEST)

            # Kiểm tra xem sản phẩm đã có trong giỏ hàng chưa
            existing_item = CartOrderItem.objects.filter(order=cart_order, product=product).first()

            if existing_item:
                # Nếu đã có, cập nhật số lượng
                existing_item.quantity += quantity
                existing_item.save()

                # Cập nhật lại tổng giá giỏ hàng sau khi cập nhật số lượng
                cart_order.total_price = sum(item.quantity * item.price for item in cart_order.items.all()) or 0
                cart_order.save()
            else:
                # Nếu chưa có, tạo mới CartOrderItem và thêm vào giỏ hàng
                CartOrderItem.objects.create(order=cart_order, product=product, quantity=quantity, price=product.price)

            # Cập nhật lại tổng giá giỏ hàng
            cart_order.total_price = sum(item.quantity * item.price for item in cart_order.items.all()) or 0
            cart_order.save()

            return Response({"message": "Sản phẩm đã được thêm vào giỏ hàng!"}, status=status.HTTP_200_OK)

        except Product.DoesNotExist:
            return Response({"error": "Sản phẩm không tồn tại."}, status=status.HTTP_400_BAD_REQUEST)
        
#Remove item:
class RemoveProductFromCartView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, product_id, format=None):
        user = request.user  # Lấy user đã đăng nhập từ request

        try:
            # Tìm giỏ hàng của người dùng
            cart_order = CartOrder.objects.filter(user=user, status='pending').first()

            if not cart_order:
                return Response({"error": "Giỏ hàng không tồn tại."}, status=status.HTTP_404_NOT_FOUND)

            # Lọc các sản phẩm trong giỏ hàng có product_id tương ứng và trả về một danh sách CartOrderItem
            cart_item = CartOrderItem.objects.filter(order=cart_order, product_id=product_id).first()

            if not cart_item:
                return Response({"error": "Sản phẩm không tồn tại trong giỏ hàng."}, status=status.HTTP_404_NOT_FOUND)

            # Cập nhật tổng giá giỏ hàng trước khi xóa sản phẩm
            cart_order.total_price -= cart_item.quantity * cart_item.price
            cart_order.save()

            # Xóa sản phẩm khỏi giỏ hàng
            cart_item.delete()

            return Response({"message": "Sản phẩm đã được xóa khỏi giỏ hàng."}, status=status.HTTP_204_NO_CONTENT)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



#CartOrderItem: 
class CartOrderItemViewSet(viewsets.ModelViewSet):
    queryset = CartOrderItem.objects.all()
    serializer_class = CartOrderItemSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # Thêm sản phẩm vào giỏ hàng
        cart_order = serializer.validated_data['order']
        product = serializer.validated_data['product']
        quantity = serializer.validated_data['quantity']
        price = product.price

        # Cập nhật tổng giá giỏ hàng sau khi thêm sản phẩm
        cart_order.total_price += quantity * price
        cart_order.save()

        # Lưu CartOrderItem vào cơ sở dữ liệu
        serializer.save()

#Thanh toán
class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Payment.objects.filter(order__user=self.request.user)  # Lọc theo người dùng