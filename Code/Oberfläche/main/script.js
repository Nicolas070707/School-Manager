// JavaScript function to display current date
function displayCurrentDate() {
    // Get today's date
    var today = new Date();
  
    // Extract the day, month, and year
    var day = today.getDate();
    var month = today.getMonth() + 1; // JavaScript counts months from 0 to 11
    var year = today.getFullYear();
  
    // Format the date as DD.MM.YYYY
    var formattedDate =
      (day < 10 ? "0" : "") +
      day +
      "." +
      (month < 10 ? "0" : "") +
      month +
      "." +
      year;
  
    // Display the formatted date in the 'date' paragraph
    document.getElementById("currentDate").textContent = formattedDate;
  }
  
  // JavaScript function to display logged in user
  function displayLoggedInUser() {
    // Benutzernamen aus localStorage lesen
    var loggedInUser = localStorage.getItem("loggedInUser");
  
    // Wenn ein Benutzer eingeloggt ist, den Benutzernamen anzeigen
    if (loggedInUser) {
      var user = JSON.parse(loggedInUser);
      document.getElementById("loggedInUser").textContent = user.name;
    } else {
      // Wenn kein Benutzer eingeloggt ist, "Nicht angemeldet" anzeigen
      document.getElementById("loggedInUser").textContent = "Nicht angemeldet";
    }
  }
  
  // Aufruf der Funktionen zur Anzeige des aktuellen Datums und des angemeldeten Benutzers
  displayCurrentDate();
  displayLoggedInUser();
  