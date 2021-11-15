
// increase and reduce product count 
window.addEventListener('click', async function(e){
  let ID
    const element = e.target.parentElement.querySelector('.plus-minus-box');
  if  (e.target.classList.contains('inc')){
    element.value = parseInt(element.value) + 1
    var quantity = element.value
     ID = e.target.previousElementSibling.value;
  }else if (e.target.classList.contains('dec')){
    element.value = parseInt(element.value) - 1
    var quantity = element.value
    ID = e.target.nextElementSibling.nextElementSibling.value;
  }
    let data = {
        'product': ID,
        'quantity': quantity,
        'user': user,     
        }
await fetch(`http://127.0.0.1:8000/api/cartitems/${ID}`, {
            headers:{
                'content-type': 'application/json'
            },
            method: 'PUT',
            body: JSON.stringify(data),
        })
    let get_response = await fetch('http://127.0.0.1:8000/api/cartitems/')
    let getcartlist = await get_response.json()
    total = 0
    count = 0
    for(let getcart of getcartlist){
        if (user == getcart.user){
            document.getElementById(`sumproduct-${ID}`).innerText = '';
            document.getElementById(`sumproduct-${ID}`).innerText += `${getcart.product.get_final_price * getcart.quantity}`
            count += getcart.quantity
            total += getcart.product.get_final_price * getcart.quantity
            totalCart.innerHTML = ``
            totalCart.innerHTML += ` <i class="mdi mdi-cart"></i>
                        <span>${count} items: </span><strong>${total} $</strong>`
            document.getElementById('cardtotalpayment').innerText = '';
            document.getElementById('cardtotalpayment').innerText = `$ ${total}`;
            document.getElementById('order-total').innerText = '';
            document.getElementById('order-total').innerText = `$ ${total}`;
    }}
})
