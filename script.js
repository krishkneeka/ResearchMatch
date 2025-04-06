const toggle = document.getElementById("darkModeToggle");

toggle.addEventListener("click", () => {
  document.body.classList.toggle("dark-mode");

  // Optional: change icon image
  if (document.body.classList.contains("dark-mode")) {
    toggle.src = "darkmode.png"; // <- use a dark mode bulb icon if you have one
  } else {
    toggle.src = "https://cdn.builder.io/api/v1/image/assets/TEMP/03961ef43cf487fbfd5436c4d9fe688589c1420a"; // <- normal bulb icon
  }
});
