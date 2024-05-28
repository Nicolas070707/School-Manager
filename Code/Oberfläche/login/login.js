function login() {
  var users = [
    {
      email: "user1@example.com",
      password: "password1",
      name: "Nicolas Theiner",
    },
    {
      email: "user2@example.com",
      password: "password2",
      name: "Michael Leeb",
    },
  ];

  var email = document.getElementById("email").value;
  var password = document.getElementById("password").value;

  var authenticatedUser = users.find(function (user) {
    return user.email === email && user.password === password;
  });

  if (authenticatedUser) {
    localStorage.setItem("loggedInUser", JSON.stringify(authenticatedUser));
    window.location.href = "/index.html";
  } else {
    alert("Falsche Email oder Passwort. Bitte versuchen Sie es erneut.");
  }
}

function signUp() {
  
}