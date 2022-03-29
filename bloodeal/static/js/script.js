// Handles the appearance/disappearance of the password
function showPassword(pass) {
var password = document.getElementById(pass);
if (password.type === "password") {
password.type = "text";
} else {
password.type = "password"}
}

//Handles the favorite button
function favorite(id) {
let favorite = document.getElementById(id);
favorite.classList.toggle("press");
}

// Handles the appearance and disappearance of a Back To Top button at the
// bottom right of the screen
const backToTopButton = document.getElementById("backToTop");
window.onscroll = function() {scrollFunction()};
function scrollFunction() {
  if (document.body.scrollTop > 100 || document.documentElement.scrollTop > 100) {
    backToTopButton.style.opacity = 1;
  } else {
    backToTopButton.style.opacity = 0;
  }
}
function backToTopFunction() {
  document.body.scrollTop = 0; // For Safari
  document.documentElement.scrollTop = 0; // For Chrome, Firefox, IE and Opera
}

//Defines constants used for modal window
const modal = document.getElementById("modal");
const modalContent = document.getElementById("modal-content");
const closeModal= document.getElementById("close-modal");
let favorites= document.getElementsByClassName("favorite");

//Closes the modal window if user clicks on the X button at the top right
if (closeModal) {
closeModal.addEventListener("click", function(event) {
    event.preventDefault();
    document.getElementById("modal").style.visibility = "hidden";
    document.getElementById("modal-content").style.visibility = "hidden";
    document.getElementById("modal-content").style.opacity = 0;
    document.getElementById("modal-content").style.transform = "translateY(40%)";
});
};

//Closes the modal window if user clicks outside of the modal window
if (modal) {
document.addEventListener("click", function(event) {
    document.getElementById("modal").style.visibility = "hidden";
    document.getElementById("modal-content").style.visibility = "hidden";
    document.getElementById("modal-content").style.opacity = 0;
    document.getElementById("modal-content").style.transform = "translateY(40%)";
});
};

//Closes the modal window if user presses Escape
if (modal) {
document.addEventListener("keyup", function(event) {
    if (event.key == "Escape") {
    document.getElementById("modal").style.visibility = "hidden";
    document.getElementById("modal-content").style.visibility = "hidden";
    document.getElementById("modal-content").style.opacity = 0;
    document.getElementById("modal-content").style.transform = "translateY(40%)";
}
});
};
