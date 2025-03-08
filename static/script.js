document.addEventListener("DOMContentLoaded", function() {
    // Navbar Toggle
    const hamburger = document.querySelector(".hamburger");
    const navLinks = document.querySelector(".nav-links");

    hamburger.addEventListener("click", () => {
        navLinks.classList.toggle("active");
    });

    // Dynamic Typing Effect
    const typedText = document.querySelector(".typed-text");
    const words = ["Simran Bhandari", "a Web Developer", "a Designer", "a Freelancer"];
    let wordIndex = 0;
    let charIndex = 0;
    let isDeleting = false;

    function typeEffect() {
        let currentWord = words[wordIndex];
        let currentText = currentWord.substring(0, charIndex);

        typedText.textContent = currentText;

        if (!isDeleting && charIndex < currentWord.length) {
            charIndex++;
            setTimeout(typeEffect, 100);
        } else if (isDeleting && charIndex > 0) {
            charIndex--;
            setTimeout(typeEffect, 50);
        } else {
            isDeleting = !isDeleting;
            wordIndex = !isDeleting ? (wordIndex + 1) % words.length : wordIndex;
            setTimeout(typeEffect, 1000);
        }
    }

    typeEffect();
});
