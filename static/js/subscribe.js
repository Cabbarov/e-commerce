let form = document.getElementById('subscribe-form');
let error_section =  document.getElementById('error-list');
form.addEventListener('submit', async function (e) {
    e.preventDefault();
    error_section.innerText = '';
    let form_data = {
        'email': form.email.value
    }
    let response = await fetch('http://localhost:8000/api/subscribe/', {
        headers: {
            'content-type': 'application/json',
            "X-CSRFToken": form.csrfmiddlewaretoken.value
        },
        method: 'POST',
        body: JSON.stringify(form_data)
    })
    let response_data = await response.json();
    let status = await response.ok;
    if(status === true){
        alert('You are successfully subscribed');
    }
    else{
        for(let error of response_data.email){
           error_section.innerHTML += `<li class="text-danger">${error}</li>`
        }
}
})