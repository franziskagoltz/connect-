"use strict";


$(".edit").on("click", function() {

    var category = $(this).val();
    var htmlAdd = "<form id='add'><input type='text' class='form-control transparency' " +
                    "id='update' placeholder='update " + category + "'></form>";

    $("#input").html(htmlAdd);

});


