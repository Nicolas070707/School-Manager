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
document.addEventListener("DOMContentLoaded", function () {
  var buttonTodo = document.getElementById("buttonTodo");
  var ol = document.querySelector("ol");
  var container = document.querySelector(".container-todo");
  var maxContainerHeight = 300; // Setze die maximale Höhe hier
  var savedTasks = JSON.parse(localStorage.getItem("tasks")) || [];

  savedTasks.forEach(function (task) {
    var listItem = document.createElement("li");
    listItem.textContent = task;
    ol.appendChild(listItem);
  });

  buttonTodo.addEventListener("click", function () {
    var inputField = document.querySelector("input[name=ListItem]");
    var toAdd = inputField.value.trim();
    if (toAdd !== "" && container.offsetHeight < maxContainerHeight) {
      var listItem = document.createElement("li");
      listItem.textContent = toAdd;
      ol.appendChild(listItem);
      savedTasks.push(toAdd);
      localStorage.setItem("tasks", JSON.stringify(savedTasks));
      inputField.value = "";
      adjustContainerHeight();
    } else if (container.offsetHeight >= maxContainerHeight) {
      alert("Maximale Höhe erreicht! Keine neuen Aufgaben mehr möglich.");
    }
  });

  document
    .querySelector("input[name=ListItem]")
    .addEventListener("keyup", function (event) {
      if (event.keyCode === 13) {
        document.getElementById("buttonTodo").click();
      }
    });

  document.addEventListener("dblclick", function (event) {
    if (event.target.tagName === "LI") {
      var taskIndex = savedTasks.indexOf(event.target.textContent);
      savedTasks.splice(taskIndex, 1);
      localStorage.setItem("tasks", JSON.stringify(savedTasks));
      event.target.classList.toggle("strike");
      event.target.style.transition = "opacity 0.5s";
      event.target.style.opacity = 0;
      setTimeout(function () {
        event.target.parentNode.removeChild(event.target);
        adjustContainerHeight();
      }, 500);
    }
  });

  ol.addEventListener("dragstart", function (event) {
    event.dataTransfer.setData("text/plain", event.target.textContent);
    event.dataTransfer.effectAllowed = "move";
  });

  ol.addEventListener("dragover", function (event) {
    event.preventDefault();
  });

  ol.addEventListener("drop", function (event) {
    event.preventDefault();
    var data = event.dataTransfer.getData("text/plain");
    var target = event.target;
    while (target.tagName !== "OL") {
      target = target.parentNode;
    }
    target.insertBefore(
      document.createElement("li"),
      event.target.nextSibling
    ).textContent = data;
  });

  function adjustContainerHeight() {
    container.style.height = "auto"; // Setze die Höhe auf automatisch zurück, um die tatsächliche Höhe der Aufgabenliste zu berücksichtigen
    var containerHeight = container.offsetHeight;
    if (containerHeight > maxContainerHeight) {
      container.style.height = maxContainerHeight + "px"; // Setze die maximale Höhe
    }
  }

  // Call adjustContainerHeight initially to set the height based on existing tasks
  adjustContainerHeight();
});

// Widgets

function drag(event) {
  event.dataTransfer.setData("text", event.target.id);
}

document.addEventListener("dragover", function (event) {
  event.preventDefault();
});

document.addEventListener("drop", function (event) {
  event.preventDefault();
  var data = event.dataTransfer.getData("text");
  var draggedElement = document.getElementById(data);

  var offsetX = event.clientX - draggedElement.clientWidth / 2;
  var offsetY = event.clientY - draggedElement.clientHeight / 2;

  draggedElement.style.left = offsetX + "px";
  draggedElement.style.top = offsetY + "px";
});

// Notes
let isDragging = false;
let offsetX, offsetY;

// Menu
function toggleAddMenu() {
  var addMenu = document.getElementById("addMenu");
  addMenu.classList.toggle("show");
  if (addMenu.classList.contains("show")) {
    var addButton = document.getElementById("addButton");
    var rect = addButton.getBoundingClientRect();
    addMenu.style.bottom = rect.height + 20 + "px";
  }
}

// Widget hinzufügen
function addNewWidget(widgetType) {
  var newWidget;
  switch (widgetType) {
    case "Cancelled Lessons":
      newWidget = createCancelledLessonsWidget();
      break;
    case "Note":
      newWidget = createNoteWidget();
      break;
    case "Upload Picture":
      newWidget = createUploadPictureWidget();
      break;
    default:
      return;
  }
  document.body.appendChild(newWidget);
  toggleAddMenu();

  const newWidgetId = "widget" + Date.now();
  newWidget.id = newWidgetId;
  document.body.appendChild(newWidget);

  // Setzen Sie das draggable Attribut und die Daten für das Drag-Event
  newWidget.draggable = true;
  newWidget.addEventListener("dragstart", (event) => {
    event.dataTransfer.setData("text/plain", newWidgetId);
  });

  var centerX = window.innerWidth / 2 - 100;
  var centerY = window.innerHeight / 2 - 75;
  newWidget.style.left = centerX + "px";
  newWidget.style.top = centerY + "px";

  makeWidgetDraggable(newWidget);
  toggleAddMenu();
}

// Widgets bewegen
function makeWidgetDraggable(widget) {
  let isDragging = false;
  let offsetX, offsetY;

  // Berechnen Sie die Grenzen basierend auf den Abmessungen des Browserfensters und den Abmessungen von Header, Footer und Sidebar
  const headerHeight = document.querySelector(".top").offsetHeight;
  const footerHeight = document.getElementById("footer").offsetHeight;
  const sidebarWidth = document.getElementById("sidebar").offsetWidth;

  widget.addEventListener("mousedown", (e) => {
    isDragging = true;
    offsetX = e.clientX - widget.getBoundingClientRect().left;
    offsetY = e.clientY - widget.getBoundingClientRect().top;
  });

  document.addEventListener("mousemove", (e) => {
    if (isDragging) {
      let x = e.clientX - offsetX;
      let y = e.clientY - offsetY;

      // Beschränken Sie x und y innerhalb der Grenzen
      x = Math.max(
        sidebarWidth,
        Math.min(x, window.innerWidth - widget.offsetWidth)
      );
      y = Math.max(
        headerHeight,
        Math.min(y, window.innerHeight - widget.offsetHeight - footerHeight)
      );

      widget.style.left = x + "px";
      widget.style.top = y + "px";
    }
  });

  document.addEventListener("mouseup", () => {
    isDragging = false;
  });
}

// Widget Inhalt
function createCancelledLessonsWidget() {
  var widget = document.createElement("div");
  widget.className = "widget draggable-widget";
  widget.draggable = true;
  widget.style.backgroundImage =
    "linear-gradient(to bottom, #1763A8 0%, #87ACD2 100%)";
  widget.innerHTML = "<h2>Cancelled lessons</h2><p>balblalbla</p>";
  makeWidgetDraggable(widget);
  addCloseButton(widget); // Add close button to widget
  return widget;
}

function createNoteWidget() {
  var widget = document.createElement("div");
  widget.className = "widget draggable-widget note-widget"; // Add 'note-widget' class for styling
  widget.draggable = true;
  widget.style.backgroundImage =
    "linear-gradient(to bottom, #FFC914 25px, #FEFEFE 25px)";

  var cover = document.createElement("div");
  cover.className = "notebook-cover";

  // Adding cover and pages to the notebook
  widget.appendChild(cover);

  // Create a container for the note content
  var contentContainer = document.createElement("div");
  contentContainer.className = "note-content-container";

  // Fügen Sie die Klasse 'widget-placeholder' dem editierbaren Element hinzu
  var content = document.createElement("div");
  content.className = "widget-content widget-placeholder";
  content.contentEditable = "true";
  content.textContent = "Write your notes here..."; // Standardtext
  contentContainer.appendChild(content);

  // Add a word counter
  var wordCounter = document.createElement("div");
  wordCounter.className = "word-counter";
  wordCounter.textContent = "Words left: 35"; // Initial value
  contentContainer.appendChild(wordCounter);

  widget.appendChild(contentContainer);

  makeWidgetDraggable(widget);
  addCloseButton(widget); // Add close button to widget

  content.addEventListener("input", function () {
    // Ändern Sie die Textfarbe auf Schwarz
    content.style.color = "black";
  });

  // Fügen Sie einen Event-Listener für das 'focus'-Ereignis hinzu
  content.addEventListener("input", function () {
    // If the text content exceeds the word limit, truncate it
    var text = content.textContent.trim();
    var words = text.split(/\s+/).filter(function (word) {
      return word.length > 0;
    });
    var remainingWords = 35 - words.length;
    if (remainingWords < 0) {
      // Truncate the text to the word limit
      var truncatedText = words.slice(0, 35).join(" ");
      content.textContent = truncatedText;
      remainingWords = 0;
    }
    wordCounter.textContent = "Words left: " + remainingWords;
  });

  // Fügen Sie einen Event-Listener für das 'blur'-Ereignis hinzu
  content.addEventListener("focus", function () {
    // Wenn der Text dem Standardtext entspricht, löschen Sie ihn
    if (content.textContent === "Write your notes here...") {
      content.textContent = "";
      content.classList.remove("widget-placeholder"); // Entfernen Sie die Klasse, um zu signalisieren, dass der Platzhaltertext entfernt wurde
    }
  });

  // Fügen Sie einen Event-Listener für das 'blur'-Ereignis hinzu
  content.addEventListener("blur", function () {
    // Wenn das Textfeld leer ist, fügen Sie den Platzhaltertext wieder ein
    if (content.textContent === "") {
      content.textContent = "Write your notes here...";
      content.classList.add("widget-placeholder"); // Fügen Sie die Klasse wieder hinzu, um anzuzeigen, dass es sich um den Platzhaltertext handelt
    }
  });

  content.addEventListener("keydown", function (event) {
    // If the number of words exceeds the limit, prevent further input
    var text = content.textContent.trim();
    var words = text.split(/\s+/).filter(function (word) {
      return word.length > 0;
    });
    if (
      words.length >= 35 &&
      event.key !== "Backspace" &&
      event.key !== "Delete"
    ) {
      event.preventDefault();
    }
  });

  return widget;
}

function createUploadPictureWidget() {
  var widget = document.createElement("div");
  widget.className = "widget draggable-widget";
  widget.draggable = true;
  widget.style.backgroundImage =
    "linear-gradient(to bottom, lightblue 0%, #87ACD2 100%)";
  widget.innerHTML =
    '<div class="picture-widget-text" onclick="selectImage()">Click to upload image</div>' +
    '<form action="/action_page.php" class="picture-widget-form" style="display: none;">' +
    '<input type="file" id="myFile" name="filename" onchange="uploadImage(this)">' +
    "</form>";
  makeWidgetDraggable(widget);
  addCloseButton(widget); // Add close button to widget
  return widget;
}

// Bild Hochladen
function selectImage() {
  document.getElementById("myFile").click();
}

function uploadImage(input) {
  var file = input.files[0];
  if (file) {
    if (!file.type.match("image/png")) {
      alert("Please select a PNG image file.");
      return;
    }
    var reader = new FileReader();
    reader.onload = function (e) {
      var img = new Image();
      img.onload = function () {
        var container = document.createElement("div");
        container.className = "draggable-widget";
        container.style.position = "absolute";
        container.style.left = "50%";
        container.style.top = "50%";
        container.style.transform = "translate(-50%, -50%)";
        container.appendChild(img);
        document.body.appendChild(container);
        makeWidgetDraggable(container);
      };
      img.src = e.target.result;
    };
    reader.readAsDataURL(file);
  }
}

function makeImageResizable(widget) {
  interact(widget)
    .resizable({
      edges: { left: true, right: true, bottom: true, top: true },
      modifiers: [
        interact.modifiers.restrictSize({
          min: { width: 100, height: 100 }, // Set minimum size
        }),
      ],
      inertia: true,
    })
    .on("resizemove", function (event) {
      var target = event.target;
      var rect = target.getBoundingClientRect();

      // Update the size
      target.style.width = event.rect.width + "px";
      target.style.height = event.rect.height + "px";

      // Calculate the center
      var centerX = rect.left + rect.width / 2;
      var centerY = rect.top + rect.height / 2;

      var translateX = parseFloat(target.getAttribute("data-x")) || 0;
      var translateY = parseFloat(target.getAttribute("data-y")) || 0;

      target.style.transform = `translate(${translateX}px, ${translateY}px)`;

      // Update InteractJS about the new size and position
      interact(target).unset();
      interact(target).resizable({
        edges: { left: true, right: true, bottom: true, top: true },
      });
    });
}

function enableWidgetDragging() {
  interact(".widget").draggable({
    onstart: function (event) {
      var target = event.target;
    },
  });
}

// Call the function to enable dragging for all widgets
enableWidgetDragging();

// Close Button

function addCloseButton(widget) {
  var closeButton = document.createElement("button");
  closeButton.textContent = "X";
  closeButton.className = "close-button";
  closeButton.style.position = "absolute";
  closeButton.style.top = "5px";
  closeButton.style.right = "5px";
  closeButton.addEventListener("click", function () {
    widget.remove(); // Remove the widget when close button is clicked
  });
  widget.appendChild(closeButton);
}

// weather

var API_KEY = "1953182eb9009119940b26400ffa251d";
var lat = "47.4167";
var lon = "9.7500";
var maxRequestsPerHour = 6;
var requestsCount = 0;

function getWeatherInfo() {
  var request_url = `https://api.openweathermap.org/data/2.5/weather?lat=${lat}&lon=${lon}&appid=${API_KEY}&lang=de`;

  fetch(request_url)
    .then((response) => response.json())
    .then((data) => {
      var weather_description = data.weather[0].description;
      var temperature = Math.round(data.main.temp - 273.15);

      document.getElementById("weather-description").textContent +=
        weather_description;
      document.getElementById("temperature").textContent += temperature + "°C";

      // Nach 10 Minuten erneut abfragen
      setTimeout(getWeatherInfo, 10 * 60 * 1000);
    })
    .catch((error) => {
      console.error("Fehler beim Abrufen der Wetterdaten:", error);
      document.getElementById("weather-description").textContent +=
        "Fehler beim Abrufen der Wetterdaten";
      document.getElementById("temperature").textContent += "Fehler";
    });

  // Zähle die Anzahl der Abfragen und überprüfe, ob die maximale Anzahl pro Stunde erreicht ist
  requestsCount++;
  if (requestsCount >= maxRequestsPerHour) {
    setTimeout(resetRequestsCount, 60 * 60 * 1000); // Setze die Anzahl der Abfragen nach einer Stunde zurück
  }
}

// Setze die Anzahl der Abfragen zurück
function resetRequestsCount() {
  requestsCount = 0;
}

// Wetterinformationen beim Laden der Seite abrufen
document.addEventListener("DOMContentLoaded", function () {
  getWeatherInfo();
});
