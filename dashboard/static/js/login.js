let maxTries = 5;
let duration = 1 * 60 * 1000;

function checkIfAllCubesFilled() {
  const allFilled = Array.from(cubes).every(cube => cube.value !== "");

  if (allFilled) {
    let timesTried = parseInt(localStorage.getItem('timesTried')) || 0;
    let timesTriedFirst = parseInt(localStorage.getItem('timesTriedFirst')) || Date.now();

    // Check if within the rate limit window
    if (timesTried >= maxTries && timesTriedFirst + duration > Date.now()) {
      const cubes = document.ectorAll(".cube");

      cubes.forEach(cube => {
        cube.style.opacity = 0.3;
        cube.value = "";
        cube.disabled = true;
      });

      return;
    }

    timesTried++;

    if (timesTried > maxTries) {
      timesTried = 1;
      timesTriedFirst = Date.now();
    }

    localStorage.setItem('timesTried', timesTried);
    localStorage.setItem('timesTriedFirst', timesTriedFirst);

    const code = Array.from(cubes).map(cube => cube.value).join("");
    console.log(code);

    crypto.subtle.digest("SHA-256", new TextEncoder().encode(code)).then(hash => {
      const hashArray = Array.from(new Uint8Array(hash));
      const hashHex = hashArray.map(byte => byte.toString(16).padStart(2, "0")).join("");

      sendDataToFlask(hashHex);
    });
  }
};





document.addEventListener("mousemove", (event) => {
  const mouseX = event.pageX;
  const mouseY = event.pageY;

  const centerX = document.documentElement.clientWidth / 2;
  const centerY = document.documentElement.clientHeight / 2;

  const moveX = (mouseX - centerX) / 300; // Adjust the divisor to control the speed of movement
  const moveY = (mouseY - centerY) / 300; // Adjust the divisor to control the speed of movement

  const rotateX = moveY * -1 + 5; // Add the initial rotation angle
  const rotateY = moveX - 15; // Subtract the initial rotation angle

  const perspective_image = document.querySelector(".command-img");
  perspective_image.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg)`;
});

document.addEventListener("paste", (event) => {
  event.preventDefault();

  const regex = /^[0-9][0-9][0-9][0-9][0-9][0-9]$/;
  if (!regex.test(event.clipboardData.getData("text/plain"))) {
    return;
  }

  const cubesInput = document.querySelectorAll(".cube");
  const text = event.clipboardData.getData("text/plain");
  const digits = text.split("");

  cubesInput.forEach((cube, index) => {
    const regex = /^[0-9]$/;
    if (!regex.test(digits[index])) {
      cube.value = "";
    }

    cube.value = digits[index] || "";

    cube.focus();
  });

  checkIfAllCubesFilled();
});


document.addEventListener("DOMContentLoaded", () => {
  const cubesInput = document.querySelectorAll(".cube");

  cubesInput.forEach(cube => {
    cube.value = "";
  });

  let timesTried = parseInt(localStorage.getItem('timesTried')) || 0;
  let timesTriedFirst = parseInt(localStorage.getItem('timesTriedFirst')) || Date.now();

  // Check if within the rate limit window
  if (timesTried >= maxTries && timesTriedFirst + duration > Date.now()) {
    const cubes = document.querySelectorAll(".cube");

    cubes.forEach(cube => {
      cube.style.opacity = 0.3;
      cube.value = "";
      cube.disabled = true;
    });

    return;
  }
});



const botTextHref = document.querySelector(".bot-text-href");

setInterval(() => {
  const sparkle = document.createElement("div");
  sparkle.classList.add("sparkle");
  sparkle.style.top = `${Math.random() * 100}%`;
  sparkle.style.left = `${Math.random() * 100}%`;
  sparkle.style.opacity = 0;
  botTextHref.appendChild(sparkle);

  sparkle.style.transition = "opacity 1s";
  sparkle.style.opacity = 1;

  sparkle.style.transform = `scale(${Math.random()})`;

  setTimeout(() => {
    sparkle.style.opacity = 0;

    setTimeout(() => {
      sparkle.remove();
    }, 1000);
  }, 1000);
}, 200);