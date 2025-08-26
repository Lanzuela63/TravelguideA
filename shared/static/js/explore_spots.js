document.addEventListener("DOMContentLoaded", function () {
  // For each button, toggle its image color on hover/focus
  document.querySelectorAll(".explore-btn").forEach(function (btn) {
    const spot = btn.getAttribute("data-spot");
    const section = btn.closest(".spot-image-section");

    btn.addEventListener("mouseenter", function () {
      section.classList.add("active");
    });
    btn.addEventListener("mouseleave", function () {
      section.classList.remove("active");
    });
    btn.addEventListener("focus", function () {
      section.classList.add("active");
    });
    btn.addEventListener("blur", function () {
      section.classList.remove("active");
    });

    // Add navigation for CamSur and Sorsogon only
    if (btn.tagName.toLowerCase() === "button") {
      btn.addEventListener("click", function () {
        if (spot === "camsur") {
          window.location.href = "/reports/camsur/"; // reported_spots_combined_camsur
        } else if (spot === "sorsogon") {
          window.location.href = "/reports/sorsogon/"; // reported_spots_combined_sorsogon
        }
      });
    }
  });
});