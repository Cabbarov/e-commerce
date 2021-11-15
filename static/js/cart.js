
let shoppingcartitemsec = document.getElementById('shopping-cart');  
let totalCart = document.getElementById('total-cart');
let mainCartPage = document.getElementById('main-cart');
let paymentTotal = document.getElementById('paymentTotal');
let cartForm = document.getElementsByClassName('addtocart-form');
for (var i = 0 ; i < cartForm.length; i++) {
    var cartelement = cartForm[i]
 };
let wishlistForm = document.getElementById('addtowishlist-form');



//change size on click 
function toggleItems() {
    $('.dropdown-menu').toggleClass('open');
  }
  
  $('.dropdown-menu li').click(function() {
    let size = $(this).text(); // get text of the clicked item
    $(".dropdown-toggle").text(size); // set text to the dropdown button 
  });
    


//change color on click and set value to input
function colorClick(clicked_color)
{
    document.getElementById('changecolor').value = ''
    document.getElementById('changecolor').value += `${clicked_color}`
}


let path = window.location.href
var loginUrl = `${path}/users/login?next=${window.location.pathname}`


if(cartelement){
cartelement.addEventListener('submit', async function(e){
    e.preventDefault();
    if(user == 'None'){
        alert('Please, login to add product to cart'),
        window.location.assign(loginUrl)
    } else {
        if (document.getElementById('product-quantity')){
            var quantity = document.getElementById('product-quantity').value
        }else{
            var quantity = 1
        };
        let product = document.getElementById('addtocart').getAttribute('data-product')
        let csrf = form.csrfmiddlewaretoken.value
        let color = document.getElementById('changecolor').value
        let size = document.getElementById('pickedsize').innerText
        console.log(color);
        let data = {
                    'product': product,
                    'quantity': quantity,
                    'user': user,
                    'color': color ,
                    'size': size, 
                    }
        let response = await fetch(`http://127.0.0.1:8000/api/cartitems/`, {
                        headers:{
                            'content-type': 'application/json',
                            "X-CSRFToken": csrf

                        },
                        method: 'POST',
                        body: JSON.stringify(data),
                    })
                    var response_data = (await response.json());
                    console.log(response_data);

        let get_response = await fetch('http://127.0.0.1:8000/api/cartitems/')
        let cartlist = await get_response.json()

        shoppingcartitemsec.innerHTML = ''
        count = 0
        total = 0
        for (let cart of cartlist){
            shoppingcartitemsec.innerHTML += `<div class="sin-itme clearfix">
            <i class="mdi mdi-close" onclick="removeproduct(${cart.product.id})"></i>
            <a class="cart-img" href="{% url 'cart' %}"><img src="${cart.product.cover_image}" alt="" /></a>
            <div class="menu-cart-text">
            <a href="#"><h5>${cart.product.title}</h5></a>
            <span>Color: <div style="margin-left: 220px; margin-top: -20px; height: 20px; width: 20px; background-color:${cart.color};"></div></span>
            <span>Size :  ${cart.size}   </span>
            <strong>${cart.product.get_final_price} $</strong>
            </div>
            </div>`;
            count += cart.quantity
            total += cart.product.get_final_price * cart.quantity
            totalCart.innerHTML = ``
            totalCart.innerHTML += ` <i class="mdi mdi-cart"></i>
                        <span>${count} items: </span><strong>${total} $</strong>`
        }             
    }
})
};



window.onload = async function (){
        count = 0
        total = 0
        let response = await fetch('http://127.0.0.1:8000/api/cartitems/')
        let getcartlist = await response.json();
        for(let getcart of getcartlist){

            productTotal = getcart.product.get_final_price * getcart.quantity
            if (user == getcart.user){
            total += productTotal 
            count += getcart.quantity
            shoppingcartitemsec.innerHTML += `<div class="sin-itme clearfix">
            <i class="mdi mdi-close" onclick="removeproduct(${getcart.product.id})"></i>
            <a class="cart-img" href="{% url 'cart'%}"><img src="${getcart.product.cover_image}" alt="" /></a>
            <div class="menu-cart-text">
                <a href="#"><h5>${getcart.product.title}</h5></a>
                <span>Color: <div style="margin-left: 220px; margin-top: -20px; height: 20px; width: 20px; background-color:${getcart.color};"></div></span>
                <span>Size :  ${getcart.size}  </span>
                <strong>${getcart.product.get_final_price} $</strong>
            </div>
        </div>`
    }}

    totalCart.innerHTML += ` <i class="mdi mdi-cart"></i>
                        <span>${count} items: </span><strong>${total} $</strong>`

    if(paymentTotal){
    paymentTotal.innerHTML += `
        <tbody>
            <tr>
                <th>Cart Subtotal</th>
                <td id="cardtotalpayment">$ ${productTotal}</td>
            </tr>
            <tr>
                <th>Shipping and Handing</th>
                <td>$00.00</td>
            </tr>
            <tr>
                <th>Vat</th>
                <td>$00.00</td>
            </tr>
        </tbody>
        <tfoot>
            <tr>
                <th class="tfoot-padd">Order total</th>
                <td class="tfoot-padd" id="order-total">$ ${productTotal}</td>
            </tr>
        </tfoot>`
    }

        for(let getcart of getcartlist){
            if (user == getcart.user && mainCartPage){
        mainCartPage.innerHTML += `<td class="td-img text-left">
        <a href="#"><img src="${getcart.product.cover_image}" alt="Add Product" /></a>
        <div class="items-dsc">
                <h5><a href="#">${getcart.product.title}</a></h5>
                <p class="itemcolor">Color : <span><div style="margin-left: 160px; margin-top: -20px; height: 20px; width: 20px; background-color:${getcart.color};"></div></span></p>
                <p class="itemcolor">Size   : <span>${getcart.size}</span></p>
        </div>
        </td>
        <td>$${getcart.product.get_final_price}</td>
        <td>
            <form action="#" method="POST"> 
                <div class="plus-minus">
                    <a class="dec qtybutton">-</a>
                    <input type="text" value="${getcart.quantity}" name="qtybutton" class="plus-minus-box">
                    <input type="hidden" value="${getcart.product.id}" id="get-product-id">
                    <a class="inc qtybutton">+</a>
                </div>
            </form>
        </td>
        <td>
            <div ><strong id="sumproduct-${getcart.product.id}"> ${getcart.product.get_final_price * getcart.quantity}</strong><span> $</span></div>
        </td>
        <td><i class="mdi mdi-close" title="Remove this product"  onclick="removeproduct(${getcart.product.id})"></i></td>`;
        }}
    };



//add to wishlist 
if (wishlistForm){
wishlistForm.addEventListener('submit', async function(e){
    e.preventDefault();
    if(user == 'None'){
        alert('Please, login to add product to Wishlist'),
        window.location.assign(loginUrl)
    }else{
        let csrf = form.csrfmiddlewaretoken.value
        let product = document.getElementById('addtoWish').getAttribute('data-product')
        let color = document.getElementById('changecolor').value
        let size = document.getElementById('pickedsize').innerText
        let data = {
            'user': user,
            'product': product,
            'color': color,
            'size': size
        }
        await fetch(`http://127.0.0.1:8000/api/wishlistitems/`, {
            headers:{
                'content-type': 'application/json',
                "X-CSRFToken": csrf
            },
            method: 'POST',
            body: JSON.stringify(data)
        })
        alert('Added to your wishlist!')
}}
)}



//remove item from wishlist
function removeitem(id){ 
    fetch(`http://127.0.0.1:8000/api/wishlistitems/${id}`, {
    method: 'DELETE'
})
location.reload()
} 



//remove product from basket  
function removeproduct(productId){ 
    fetch(`http://127.0.0.1:8000/api/cartitems/${productId}`, {
    method: 'DELETE'
})
location.reload()
};





