document.getElementById('process-form').addEventListener('submit', function(event) {
  const progressBar = document.getElementById('progress-bar');
  progressBar.style.width = '0%';
  const interval = setInterval(() => {
      let width = parseInt(progressBar.style.width);
      if (width >= 100) {
          clearInterval(interval);
      } else {
          progressBar.style.width = (width + 10) + '%';
      }
  }, 300);
});
