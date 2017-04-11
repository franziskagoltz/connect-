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

    // handling submit event of edit event: needs to be in callback, otherwise the 
    // form with the add-id is not in the DOM -- submit event won't work 
    $("#add").on("submit", function() {

        var updatedVal = $("#update").val();

        // sending post request to server to handle update & store it in db
        $.post("/handle-update", {"category": category, "value": updatedVal, "id": c_id});
    });

});


