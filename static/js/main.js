// static/js/main.js

document.addEventListener('DOMContentLoaded', function() {
  const slider = document.querySelector('.slider');
  if (!slider) return;

  const slides = slider.querySelectorAll('.slides img');
  const prevBtn = slider.querySelector('.arrow.prev');
  const nextBtn = slider.querySelector('.arrow.next');
  let current = 0;
  let timer;

  function showSlide(index) {
    slides.forEach((img, i) => {
      if (i === index) {
        img.classList.add('active');
      } else {
        img.classList.remove('active');
      }
    });
  }

  function startAuto() {
    timer = setInterval(() => {
      current = (current + 1) % slides.length;
      showSlide(current);
    }, 3000);
  }

  function stopAuto() {
    clearInterval(timer);
  }

  // Arrow click handlers
  prevBtn.addEventListener('click', () => {
    stopAuto();
    current = (current - 1 + slides.length) % slides.length;
    showSlide(current);
    startAuto();
  });
  nextBtn.addEventListener('click', () => {
    stopAuto();
    current = (current + 1) % slides.length;
    showSlide(current);
    startAuto();
  });

  // Pause on hover, resume on leave
  slider.addEventListener('mouseenter', stopAuto);
  slider.addEventListener('mouseleave', startAuto);

  // Kick it off
  showSlide(current);
  startAuto();
});
