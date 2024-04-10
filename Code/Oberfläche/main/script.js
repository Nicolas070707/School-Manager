
function displayCurrentDate() {
    // Get today's date
    var today = new Date();
  
    var day = today.getDate();
    var month = today.getMonth() + 1; 
    var year = today.getFullYear();
  

    var formattedDate =
      (day < 10 ? "0" : "") +
      day +
      "." +
      (month < 10 ? "0" : "") +
      month +
      "." +
      year;
  

    document.getElementById("currentDate").textContent = formattedDate;
  }
  

  function displayLoggedInUser() {
   
    var loggedInUser = localStorage.getItem("loggedInUser");
  
 
    if (loggedInUser) {
      var user = JSON.parse(loggedInUser);
      document.getElementById("loggedInUser").textContent = user.name;
    } else {

      document.getElementById("loggedInUser").textContent = "Nicht angemeldet";
    }
  }

  displayCurrentDate();
  displayLoggedInUser();
  
  function togglePopup() {
    var popup = document.getElementById('infoPopup');
    if (popup.style.display === 'block') {
        popup.style.display = 'none';
    } else {
        popup.style.display = 'block';
    }
}
 