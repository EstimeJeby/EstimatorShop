import json

from .models import *

def cookieCart(request):
    try:

        cart =json.loads(request.COOKIES['cart'])
    except:
        cart ={}
    print('cart',cart)
    items =[]
    order ={'get_cart_total':0 ,'get_cart_items':0,'shipping':False}
    cartItems= order['get_cart_items']

    for i in cart:
        try:
            cartItems+=cart[i]['quantity']
            product = Product.objects.get(id=i)
            total =(product.prix * cart[i]["quantity"])
            order['get_cart_total']+=total
            order['get_cart_items']+=cart[i]['quantity']

            item ={
                'product':{
                    'id':product.id,
                    'name':product.name,
                    'prix':product.prix,
                    'image':product.image,
                    'detail':product.detail,

                },
                'quantity':cart[i]["quantity"],
                'get_total':total

            }
            items.append(item)

            if product.digital == False:
                order['shipping'] = True
        except:
            pass

    return {'cartItems': cartItems, 'order':order,'items':items}