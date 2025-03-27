import { loadGraphData } from './graph.js';

document.addEventListener('DOMContentLoaded', () => {
  const folderInput = document.getElementById('folderPath');
  const status = document.getElementById('status');
  const analyzeBtn = document.getElementById('analyzeBtn');

  analyzeBtn.addEventListener('click', () => {
    const folderPath = folderInput.value.trim();
    if (!folderPath) {
      status.textContent = 'Please enter a folder path.';
      return;
    }

    status.textContent = 'Analyzing...';

    fetch('/upload', {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: new URLSearchParams({ folderPath })
    })
    .then(res => res.json())
    .then(res => {
      if (res.status === 'ok') {
        status.textContent = 'Analysis complete. Loading graph...';
        setTimeout(() => {
          loadGraphData(); // re-render the graph
          status.textContent = '';
        }, 1000);
      } else {
        status.textContent = `Error: ${res.message}`;
      }
    })
    .catch(err => {
      status.textContent = 'Request failed.';
      console.error(err);
    });
  });

  loadGraphData(); // initial render
});
