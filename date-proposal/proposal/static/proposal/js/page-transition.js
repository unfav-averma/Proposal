const pageTransition = document.getElementById("pageTransition") ||
    document.querySelector(".page-transition");


/* PAGE LOAD */
window.addEventListener("pageshow", function() {

    if (pageTransition) {
        pageTransition.classList.remove("active");
    }

});


/* PAGE CHANGE */
function goToPage(url) {

    if (pageTransition) {
        pageTransition.classList.add("active");
    }

    setTimeout(function() {

        window.location.href = url;

    }, 700);

}