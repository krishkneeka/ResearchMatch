const toggle = document.getElementById("darkModeToggle");

toggle.addEventListener("click", () => {
  document.body.classList.toggle("dark-mode");

  // Optional: change icon image
  if (document.body.classList.contains("dark-mode")) {
    toggle.src = "lightbulb-dark.png"; // <- use a dark mode bulb icon if you have one
  } else {
    toggle.src = "lightbulb.png"; // <- normal bulb icon
  }
});
