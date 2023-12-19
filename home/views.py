from django.shortcuts import render
from .models import Product,Categorie,Customer,Order,OrderItem,ShippingAdress
from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy,reverse
from django.views.generic import RedirectView
from django.contrib import messages
from .forms import  CreateProduct
from django.http import JsonResponse
import json
import datetime
from .utils import cookieCart

from django.views.generic import (
    ListView,
    DetailView,
    UpdateView,
    DeleteView
)


def home(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items 
    else:
        cookieData = cookieCart(request)
        cartItems = cookieData['cartItems']
        items = cookieData['items']
        order = cookieData['order']
       
    context = {
        'product': Product.objects.all(),
        'cartItems': cartItems
       
    }
    return render(request,'blog/home.html',context)



class ProductListView(ListView):
    model = Product
    template_name = 'blog/home.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'product'
    ordering = ['-date_posted']
    paginate_by = 5


class UserProductListView(ListView):
    model = Product
    template_name = 'blog/user_product.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Product.objects.filter(author=user).order_by('-date_posted')
    

class ProductDetailView(DetailView):
    model = Product
    template_name = 'blog/product_detail.html'



def UploadProduct(request):
    form = CreateProduct()

    if request.method == 'POST':
        form = CreateProduct(request.POST,request.FILES)
        if form.is_valid():
            form.instance.author= request.user
            form.save()
            messages.success(request,f'A few product  has been Created')
            return redirect('blog-home')

        else:
            messages.info(request,f'error the Post is not created!')
            return redirect('post-create')

    context ={
        'form':form
    }
    
    return render(request,'blog/uploadFile.html',context)



class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Product
    fields = ['name', 'content']
    template_name = 'blog/uploadfile.html'
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Product
    template_name = 'blog/post_confirm_delete.html'
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        cookieData = cookieCart(request)
        cartItems = cookieData['cartItems']
        items = cookieData['items']
        order = cookieData['order']

    context={'items':items, 'order':order}
    return render(request,'blog/cart.html',context)

def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        cookieData = cookieCart(request)
        cartItems = cookieData['cartItems']
        items = cookieData['items']
        order = cookieData['order']

    context={'items':items, 'order':order}
    return render(request,'blog/checkout.html',context)



def updateItem(request):
    if request.method =='POST':
        data = json.loads(request.body)
        productId = data['productId']
        action = data['action']
     
        customer = request.user.customer
        product = Product.objects.get(id=productId)
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        orderItem,created  = OrderItem.objects.get_or_create(Product=product, Order=order) 

        if action == 'add':
            orderItem.quantity =(orderItem.quantity + 1)
        elif action== ' remove':
            orderItem.quantity = (orderItem.quantity - 1)
        orderItem.save()
        if orderItem.quantity <= 0:
            orderItem.delete()
        return JsonResponse('Item was added', safe=False)
    

def processOrder(request):
    if request.method =='POST':
        transaction_id = datetime.datetime.now().timestamp()
        data = json.loads(request.body)
        if request.user.is_authenticated:
            customer = request.user.customer
            
            order, created = Order.objects.get_or_create(customer=customer, complete=False)
            total = float(data['form']['total'])
            order.transaction_id = transaction_id

            if total == float(order.get_cart_total):
                order.complete = True
            order.save()

            if Order.shipping == True:
                ShippingAdress.objects.create(
                    customer= customer,
                    Order = Order,
                    address = data['shipping']['address'],
                    city = data['shipping']['city'],
                    state = data['shipping']['state'],
                    zipcode = data['shipping']['zipcode']

                )

        
        else:
            print('User is not loggin')
      
    return JsonResponse('Payment Complete', safe=False)