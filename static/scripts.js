const form = document.getElementById("shortener_form");

form.addEventListener("submit", async function (e) {
  e.preventDefault();

  let urlInput = document.getElementById("url");
  let sizeInput = document.getElementById("size");
  let errorMsg = document.getElementById("error-message");
  let successMsg = document.getElementById("success-message");

  errorMsg.style.display = "none";
  successMsg.style.display = "none";
  errorMsg.innerText = "";
  successMsg.innerHTML = "";

  let sizeForm = 8;

  if (sizeInput.value.trim() == "") {
    sizeForm = 8;
  } else {
    sizeForm = parseInt(sizeInput.value);
  }

  let data = {
    url_input: urlInput.value,
    size_input: sizeForm
  };

  try {
    const res = await fetch("/api/shorten", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    });

    const resData = await res.json();

    if (!res.ok) {
      errorMsg.innerText = resData.detail || "An unknown error has occurred.";
      errorMsg.style.display = "block";
      return;
    }

    const shortUrl = `${window.location.origin}/api/shorten/${resData.hash}`;

    successMsg.innerHTML = `
      Your shortened URL is:
      <a style="color: white" href="${shortUrl}" target="_blank">
        ${shortUrl}
      </a>
    `;
    successMsg.style.display = "block";
    urlInput.value = "";
  } catch (err) {
    errorMsg.innerText = "Couldn't connect to the server.";
    errorMsg.style.display = "block";
    console.error(err);
  }
});
