// Heutiges Datum
function displayCurrentDate() {
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

// Loged In User
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




// INFO
function togglePopup() {
  var popup = document.getElementById("infoPopup");
  if (popup.style.display === "block") {
    popup.style.display = "none";
  } else {
    popup.style.display = "block";
  }
}


// Todo
document.addEventListener('DOMContentLoaded', function() {
  var buttonTodo = document.getElementById('buttonTodo');
  var ol = document.querySelector('ol');
  var container = document.querySelector('.container-todo');
  var maxContainerHeight = 300; // Setze die maximale Höhe hier
  var savedTasks = JSON.parse(localStorage.getItem('tasks')) || [];

  savedTasks.forEach(function(task) {
    var listItem = document.createElement('li');
    listItem.textContent = task;
    ol.appendChild(listItem);
  });

  buttonTodo.addEventListener('click', function() {
    var inputField = document.querySelector('input[name=ListItem]');
    var toAdd = inputField.value.trim();
    if (toAdd !== '' && container.offsetHeight < maxContainerHeight) {
      var listItem = document.createElement('li');
      listItem.textContent = toAdd;
      ol.appendChild(listItem);
      savedTasks.push(toAdd);
      localStorage.setItem('tasks', JSON.stringify(savedTasks));
      inputField.value = '';
      adjustContainerHeight();
    } else if (container.offsetHeight >= maxContainerHeight) {
      alert('Maximale Höhe erreicht! Keine neuen Aufgaben mehr möglich.');
    }
  });

  document.querySelector('input[name=ListItem]').addEventListener('keyup', function(event) {
    if (event.keyCode === 13) {
      document.getElementById('buttonTodo').click();
    }
  });

  document.addEventListener('dblclick', function(event) {
    if (event.target.tagName === 'LI') {
      var taskIndex = savedTasks.indexOf(event.target.textContent);
      savedTasks.splice(taskIndex, 1);
      localStorage.setItem('tasks', JSON.stringify(savedTasks));
      event.target.classList.toggle('strike');
      event.target.style.transition = 'opacity 0.5s';
      event.target.style.opacity = 0;
      setTimeout(function() {
        event.target.parentNode.removeChild(event.target);
        adjustContainerHeight();
      }, 500);
    }
  });

  ol.addEventListener('dragstart', function(event) {
    event.dataTransfer.setData('text/plain', event.target.textContent);
    event.dataTransfer.effectAllowed = 'move';
  });

  ol.addEventListener('dragover', function(event) {
    event.preventDefault();
  });

  ol.addEventListener('drop', function(event) {
    event.preventDefault();
    var data = event.dataTransfer.getData('text/plain');
    var target = event.target;
    while (target.tagName !== 'OL') {
      target = target.parentNode;
    }
    target.insertBefore(document.createElement('li'), event.target.nextSibling).textContent = data;
  });

  function adjustContainerHeight() {
    container.style.height = 'auto'; // Setze die Höhe auf automatisch zurück, um die tatsächliche Höhe der Aufgabenliste zu berücksichtigen
    var containerHeight = container.offsetHeight;
    if (containerHeight > maxContainerHeight) {
      container.style.height = maxContainerHeight + 'px'; // Setze die maximale Höhe
    }
  }

  // Call adjustContainerHeight initially to set the height based on existing tasks
  adjustContainerHeight();
});
