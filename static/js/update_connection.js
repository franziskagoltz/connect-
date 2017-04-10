"use strict";


// handeling click event on edit icon: generates a form and input field
$(".edit").on("click", function() {

    // grabbing the value of the clicked event so we can keep track of the attribute 
    // that is supposed to get updated
    var category = $(this).val();

    // storin the form that will be rendered in a var
    var htmlAdd = "<form id='add'><input type='text' class='form-control transparency' " +
                    "id='update' placeholder='update " + category + "'></form>";

    // appending the form to the html div
    $("#input").html(htmlAdd);

});


