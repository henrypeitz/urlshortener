const form = document.getElementById('shortener_form')

form.addEventListener('submit', function(e) {

    e.preventDefault();

    let urlInput = document.getElementById('url');
    urlInput = urlInput.value 

    const data = {
        urlInput: urlInput
    }

    if(urlInput === "" || urlInput == null) {
        alert("Invalid URL")
        return;
    }

    const res = fetch('http://127.0.0.1:8000/shorten', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    }).catch(error => {
        console.log("Something went very wrong...")
    })

    if(!res.ok) {
        alert("Something went wrong!")
        return;
    } else {
        console.log("Everything went great in this shit!")
    }

})