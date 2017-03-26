// This is called with the results from from FB.getLoginStatus().
 
  // object to store user data we get back from fb oauth
  var user_data = {};

  window.fbAsyncInit = function() {
  FB.init({
    appId      : fbAPI,
    cookie     : true,  // enable cookies to allow the server to access 
                        // the session
    xfbml      : true,  // parse social plugins on this page
    version    : 'v2.8' // use graph api version 2.8
  });

 };


  function fblogin() {
    console.log("in fblogin function");
    FB.login(function(response) {
        console.log("in FB.set function");
        if (response.authResponse) {
          console.log('Welcome!  Fetching your information.... ');
          console.log(response.authResponse.accessToken);
          user_data["token"] = response.authResponse.accessToken;
          FB.api('/me', {fields:['email', 'first_name', 'last_name', 'id', 'locale', 'picture',]}, function(response) {

          user_data["email"] = response.email;
          user_data["first_name"] = response.first_name;
          user_data["last_name"] = response.last_name;
          user_data["fb_id"] = response.id;
          user_data["locale"] = response.locale;
          user_data["picture"] = response.picture;
          // user_data["user_friends"] = response.user_friends;

          console.log(user_data);

          $.post("/fb-oauth", user_data, function() {
            console.log("user data sent successfully from fblogin()");
            window.location.href = "http://localhost:5000/view-connections";
          });


           console.log('Good to see you, ' + response.first_name + '.');
         });
          
        } else {
         console.log('User cancelled login or did not fully authorize.');
        }
    }, {scope: 'public_profile,email,user_friends'});
  }


  // Load the SDK asynchronously
  (function(d, s, id) {
    var js, fjs = d.getElementsByTagName(s)[0];
    if (d.getElementById(id)) return;
    js = d.createElement(s); js.id = id;
    js.src = "//connect.facebook.net/en_US/sdk.js";
    fjs.parentNode.insertBefore(js, fjs);
  }(document, 'script', 'facebook-jssdk'));

   