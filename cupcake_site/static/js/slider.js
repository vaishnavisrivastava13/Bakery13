let index = 0;
const slides = document.querySelectorAll(".slide");
const next = document.querySelector(".right");
const prev = document.querySelector(".left");

function showSlide(i) {
    slides.forEach(slide => slide.style.display = "none");
    slides[i].style.display = "block";
}

next.onclick = () => {
    index = (index + 1) % slides.length;
    showSlide(index);
};

prev.onclick = () => {
    index = (index - 1 + slides.length) % slides.length;
    showSlide(index);
};

setInterval(() => {
    index = (index + 1) % slides.length;
    showSlide(index);
}, 3000);

showSlide(index);

