// ===============================
// Infinite Auto Scrolling Carousel
// ===============================

const carousel = document.querySelector(".carousel");

if (carousel) {

    // Duplicate all cards for seamless looping
    carousel.innerHTML += carousel.innerHTML;

    let speed = 1;

    function autoScroll() {

        carousel.scrollLeft += speed;

        // Reset after reaching half (original content)
        if (carousel.scrollLeft >= carousel.scrollWidth / 2) {
            carousel.scrollLeft = 0;
        }

        requestAnimationFrame(autoScroll);
    }

    autoScroll();

    // Pause on hover
    carousel.addEventListener("mouseenter", () => {
        speed = 0;
    });

    // Resume on mouse leave
    carousel.addEventListener("mouseleave", () => {
        speed = 1;
    });

}