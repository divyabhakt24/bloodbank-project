// Counter Animation
document.addEventListener("DOMContentLoaded", () => {
  const counters = document.querySelectorAll(".counter");

  counters.forEach(counter => {
    const updateCount = () => {
      const target = +counter.getAttribute("data-target");
      const count = +counter.innerText;
      const speed = 200; // lower = faster
      const increment = target / speed;

      if (count < target) {
        counter.innerText = Math.ceil(count + increment);
        setTimeout(updateCount, 10);
      } else {
        counter.innerText = target;
      }
    };
    updateCount();
  });

  // FAQ Toggle
  const questions = document.querySelectorAll(".faq .question");
  questions.forEach(q => {
    q.addEventListener("click", () => {
      const answer = q.nextElementSibling;
      answer.style.display = answer.style.display === "block" ? "none" : "block";
    });
  });
});
