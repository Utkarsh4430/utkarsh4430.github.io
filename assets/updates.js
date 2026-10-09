// Progressive enhancement: the complete timeline remains scrollable without JavaScript.
(() => {
  const timeline = document.querySelector('.news-scroll');
  const frame = document.querySelector('.news-window');
  const button = document.querySelector('.news-more');
  if (!timeline || !frame || !button) return;

  const update = () => {
    const end = timeline.scrollHeight - timeline.clientHeight;
    const atEnd = timeline.scrollTop >= end - 2;
    frame.classList.toggle('is-scrolled', timeline.scrollTop > 2);
    frame.classList.toggle('at-end', atEnd);
    button.hidden = end <= 2;
    button.textContent = atEnd ? 'Back to latest ↑' : 'Older updates ↓';
  };
  button.addEventListener('click', () => {
    const atEnd = timeline.scrollTop >= timeline.scrollHeight - timeline.clientHeight - 2;
    const behavior = window.matchMedia('(prefers-reduced-motion: reduce)').matches ? 'instant' : 'smooth';
    if (atEnd) timeline.scrollTo({ top: 0, behavior });
    else timeline.scrollBy({ top: timeline.clientHeight * .8, behavior });
  });
  timeline.addEventListener('scroll', update, { passive: true });
  window.addEventListener('resize', update);
  update();
})();
