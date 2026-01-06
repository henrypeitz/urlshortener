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

    if(res.status === 400) {
        console.log("Your URL seems invalid.")
    }

    let resData = await res.json()
    console.log(resData)
    alert(`Your shorten URL is: http://localhost:8000/shorten/${resData}`)
    
})