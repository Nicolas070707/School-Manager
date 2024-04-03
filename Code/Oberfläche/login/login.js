function login() {
  // Dummy-Benutzerdaten für das Beispiel
  var users = [
    {
      email: "user1@example.com",
      password: "password1",
      name: "Nicolas Theiner",
    },
    {
      email: "user2@example.com",
      password: "password2",
      name: "Erika Musterfrau",
    },
  ];

  var email = document.getElementById("email").value;
  var password = document.getElementById("password").value;

  var authenticatedUser = users.find(function (user) {
    return user.email === email && user.password === password;
  });

  if (authenticatedUser) {
    // Benutzer in localStorage speichern
    localStorage.setItem("loggedInUser", JSON.stringify(authenticatedUser));
    // Weiterleitung zur index.html-Seite
    window.location.href = "../main/index.html";
  } else {
    alert("Falsche Email oder Passwort. Bitte versuchen Sie es erneut.");
  }
}
