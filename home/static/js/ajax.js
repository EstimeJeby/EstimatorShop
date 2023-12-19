

var updatebtn = document.getElementsByClassName('Update-cart');

for(var i=0; i< updatebtn.length; i++)
{
    updatebtn[i].addEventListener('click', function(e)
    {
        var productId = this.dataset.product
        var action = this.dataset.action

        console.log('productId:', productId ,'action:',action)
        console.log('user:', user)

     if(user === 'AnonymousUser')
     {
        console.log('not loggin...')
        // addCookieItem(productId, action) 
     }
     else{

        UpdateUserOrder(productId, action)
    }

    })

}

function addCookieItem(productId, action){
    console.log('not loggin...')
    if (action == 'add'){
        if(cart[productId]==undefined){
            cart[productId]={'quantity':1}

        }else{
            cart[productId]['quantity'] +1

        }
    }
    if(action == 'remove'){
        cart[productId]['quantity'] -=1
        if (cart[productId]['quantity'] <= 0){
            console.log('remove the Item')
            delete cart[productId]
        }
    }
    console.log('cart',cart)
    document.cookie= 'cart'+JSON.stringify(cart) + ";domain=;path=/"
}

function UpdateUserOrder(productId, action){
    console.log('user is log in sending data...')

    const url = '/update_Item/';

    fetch(url,{
        method:'POST',
        headers: {
            'Content-Type':'application/json',
            'X-CSRFToken': csrftoken,
        },
        body:JSON.stringify({ 'productId':productId, 'action':action})
    })

    .then((response) =>{
        if(!response.ok){
            //error processing
            throw 'Error'
        }
        return response.json()
    })

    .then((data) =>{
        console.log('data:', data)
        location.reload()
    })
}