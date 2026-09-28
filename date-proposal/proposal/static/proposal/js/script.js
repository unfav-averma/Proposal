console.log("JavaScript is connected!");
const message = document.getElementById("message");
const noBtn = document.getElementById("noBtn");
const yesBtn = document.getElementById("yesBtn");
let noClicks = 0;

noBtn.addEventListener("click", function() {
    noClicks++;

    console.log(noClicks);
    console.log(yesBtn);
    yesBtn.style.width = `${180 + noClicks * 15}px`;
    yesBtn.style.padding = `${12 + noClicks * 2}px 20px`;
    yesBtn.style.fontSize = `${20 + noClicks * 2}px`;

      if (noClicks === 1) {
        message.textContent = "Aww, are you sure? 🥺";
        message.style.color = "#8f3048";
        message.classList.add("no-message");}
    else if (noClicks === 2) {

    message.textContent = "Maybe give it another thought? 💗";
    message.style.color = "#9b4d6e";

} else if (noClicks === 3) {

    message.textContent = "I'm running out of arguments 😭";
    message.style.color = "#a65363";

} else if (noClicks === 4) {

    message.textContent = "Okay... I’ll stop asking 😌";
    message.style.color = "#7d4655";
    noBtn.classList.add("disappear");
}
});

yesBtn.addEventListener("click", function() {

    const csrfToken = document.querySelector(
        "[name=csrfmiddlewaretoken]"
    ).value;

    fetch("/start-proposal/", {
        method: "POST",
        headers: {
            "X-CSRFToken": csrfToken
        }
    })
        .then(function(response) {
            if (!response.ok) {
                throw new Error("Server returned an error: " + response.status);
            }

            return response.json();
        })
        .then(function(data) {

            if (data.success) {

                window.location.href = "/date/";

            }

        })
        .catch(function(error) {

            console.error("Error starting proposal:", error);

        });

});
