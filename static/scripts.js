const form = document.getElementById('shortener_form')

form.addEventListener('submit', async function(e) {

    e.preventDefault();

    let urlInput = document.getElementById('url');
    urlInput = urlInput.value 

    const data = {
        url_input: urlInput
    }

    if(urlInput === "" || urlInput == null) {
        alert("Invalid URL")
        return;
    }

    const res = await fetch('http://localhost:8000/shorten', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    }).catch(error => {
        console.log(error)
        console.log("Something went very wrong...")
    })

    let resData = await res.json()
    alert(`Your shorten URL is: http://localhost:8000/shorten/${resData}`)
    
})