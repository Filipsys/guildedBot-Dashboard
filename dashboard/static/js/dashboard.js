const logoutBtn = document.querySelector(".logout-container");

logoutBtn.addEventListener("mouseover", () => {
  const intervalSparkles = setInterval(() => {
    const sparkle = document.createElement("div");
    sparkle.classList.add("sparkle");
    sparkle.style.top = `${Math.random() * 120}%`;
    sparkle.style.left = `${Math.random() * 120}%`;
    sparkle.style.opacity = 0;
    logoutBtn.appendChild(sparkle);

    setTimeout(() => {
      sparkle.style.opacity = 1;
    }, 100);

    sparkle.style.transform = `scale(${Math.random()})`;

    setTimeout(() => {
      sparkle.style.opacity = 0;

      setTimeout(() => {
        sparkle.remove();
      }, 1000);
    }, 1000);
  }, 100);

  logoutBtn.addEventListener("mouseout", () => {
    clearInterval(intervalSparkles);
  });
});


const filterTuneHover = document.querySelector(".filters-div");

filterTuneHover.addEventListener("mouseover", () => {
  const oneFilter = document.querySelector(".one-filter");
  const sevenFilter = document.querySelector(".seven-filter");
  const eightFilter = document.querySelector(".thirty-filter");

  oneFilter.style.display = "block";
  sevenFilter.style.display = "block";
  eightFilter.style.display = "block";


  filterTuneHover.addEventListener("mouseout", () => {
    oneFilter.style.display = "none";
    sevenFilter.style.display = "none";
    eightFilter.style.display = "none";

    removeEventListener("mouseout");
  });
});


// window.addEventListener('DOMContentLoaded', function() {
//   var webpImages = document.querySelectorAll('img[src$=".webp"]');

//   webpImages.forEach(function(img) {
//       img.setAttribute('loading', 'lazy'); // Optional: lazy load the images
//       img.setAttribute('draggable', 'false'); // Optional: disable dragging
//       img.setAttribute('alt', ''); // Optional: provide alt text for accessibility
//       img.addEventListener('mousedown', function(event) {
//           event.preventDefault(); // Prevent the default behavior on mousedown
//       });
//   });
// });

const recentActivity = document.querySelector(".recent-activity");
recentActivity.addEventListener('contextmenu', (event) => {
  event.preventDefault();

  setTimeout(() => {

    try {
      document.querySelector(".context-menu").remove();
    } catch (error) {
      // Do nothing
    }

    const contextMenu = document.createElement("div");
    contextMenu.classList.add("context-menu");
    contextMenu.style.top = `${event.clientY}px`;
    contextMenu.style.left = `${event.clientX}px`;
    contextMenu.style.display = "block";
    

    const exportOption = document.createElement("div");
    exportOption.textContent = "Export as CSV";

    const copyOption = document.createElement("div");
    copyOption.textContent = "Copy";

    contextMenu.appendChild(exportOption);
    contextMenu.appendChild(copyOption);

    document.body.appendChild(contextMenu);


    copyOption.addEventListener("click", () => {
      const text = event.target.textContent;
      navigator.clipboard.writeText(text);
    });

    const closeContextMenu = document.addEventListener("click", () => {
      contextMenu.remove();

      document.removeEventListener("click", closeContextMenu);
    });
  }, 10);
});

document.addEventListener('contextmenu', (event) => {
  try {
    document.querySelector(".context-menu").remove();
  } catch (error) {
    // Do nothing
  }
});