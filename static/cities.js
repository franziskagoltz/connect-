"use strict";

function filter_cities(data) {

    // instantiating an array of contacts living in the selected city
    var contacts = [];

// looping over json result
    for (var i = 0; i < data[0].length; i++) {

        // adding first name of contact to contacts array with html elements
        contacts.push('<li>'+data[0][i].first_name+'</li');
        
    };

    // updating the DOM with the filtered contacts
    $("#filterd").html(contacts);
}


$('.city').on('click', function() {

    var city = $(this).val();

    console.log(city);

    $.post("/cities.json", {"city": city}, filter_cities);

});
