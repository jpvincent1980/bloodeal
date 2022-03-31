// Handles the import of the IMDB rating
function imdb(d,s,id) {
var js,stags=d.getElementsByTagName(s)[0];
if(d.getElementById(id)) {
return;
}
js=d.createElement(s);
js.id=id;
js.src="https://ia.media-imdb.com/images/G/01/imdb/plugins/rating/js/rating.js";
stags.parentNode.insertBefore(js,stags);
}

imdb(document,"script","imdb-rating-api")

// Handles the appearance/disappearance of the password
function showPassword(pass) {
var password = document.getElementById(pass);
if (password.type === "password") {
password.type = "text";
} else {
password.type = "password"}
}

// Handles the csrf token
function getCookie(c_name)
{
    if (document.cookie.length > 0)
    {
        c_start = document.cookie.indexOf(c_name + "=");
        if (c_start != -1)
        {
            c_start = c_start + c_name.length + 1;
            c_end = document.cookie.indexOf(";", c_start);
            if (c_end == -1) c_end = document.cookie.length;
            return unescape(document.cookie.substring(c_start,c_end));
        }
    }
    return "";
 }

//Handles the favorite button
function favorite(id, pk, type) {

    let favorite = document.getElementById(id);
    favorite.classList.toggle("press");

    $.ajaxSetup({
        headers: { "X-CSRFToken": getCookie("csrftoken") }
    });

    $.ajax({
        url: "/profiles/add-to-favorite/",
        data: {
//            'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val(),
            'type': type,
            'pk': pk
        },
        type: "POST",
        success: function (json) {
            location.reload();
            console.log(json);
        },
        error: function (xhr, errmsg, err) {
            console.log(errmsg);
        }
    });
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
