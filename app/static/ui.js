import * as THREE from 'https://esm.sh/three';
import { loadGraphData, Graph } from './graph.js';

document.addEventListener('DOMContentLoaded', () => {
  const folderInput = document.getElementById('folderPath');
  const status = document.getElementById('status');
  const analyzeBtn = document.getElementById('analyzeBtn');
  const cameraInfo = document.getElementById('cameraInfo');

  const resetCamBtn = document.getElementById('resetCamBtn');
  const zoomInBtn = document.getElementById('zoomInBtn');
  const zoomOutBtn = document.getElementById('zoomOutBtn');
  const tiltUpBtn = document.getElementById('tiltUpBtn');
  const tiltDownBtn = document.getElementById('tiltDownBtn');
  const orbitLeftBtn = document.getElementById('orbitLeftBtn');
  const orbitRightBtn = document.getElementById('orbitRightBtn');
  const rollLeftBtn = document.getElementById('rollLeftBtn');
  const rollRightBtn = document.getElementById('rollRightBtn');

  const tiltStep = 10;
  const orbitStep = 10;
  const rollStep = 0.05;

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
            loadGraphData();
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

  resetCamBtn.addEventListener('click', () => {
    Graph.cameraPosition({ x: 0, y: 0, z: 300 }, null, 1000);
  });

  zoomInBtn.addEventListener('click', () => {
    const cam = Graph.camera();
    cam.position.z -= 50;
  });

  zoomOutBtn.addEventListener('click', () => {
    const cam = Graph.camera();
    cam.position.z += 50;
  });

  tiltUpBtn.addEventListener('click', () => {
    Graph.camera().position.y += tiltStep;
  });

  tiltDownBtn.addEventListener('click', () => {
    Graph.camera().position.y -= tiltStep;
  });

  orbitLeftBtn.addEventListener('click', () => {
    const cam = Graph.camera();
    const angle = orbitStep * (Math.PI / 180);
    const { x, z } = cam.position;
    const r = Math.sqrt(x * x + z * z);
    const theta = Math.atan2(z, x) + angle;
    cam.position.x = r * Math.cos(theta);
    cam.position.z = r * Math.sin(theta);
  });

  orbitRightBtn.addEventListener('click', () => {
    const cam = Graph.camera();
    const angle = -orbitStep * (Math.PI / 180);
    const { x, z } = cam.position;
    const r = Math.sqrt(x * x + z * z);
    const theta = Math.atan2(z, x) + angle;
    cam.position.x = r * Math.cos(theta);
    cam.position.z = r * Math.sin(theta);
  });

  rollLeftBtn.addEventListener('click', () => {
    Graph.camera().up.applyAxisAngle(new THREE.Vector3(0, 0, 1), rollStep);
  });

  rollRightBtn.addEventListener('click', () => {
    Graph.camera().up.applyAxisAngle(new THREE.Vector3(0, 0, 1), -rollStep);
  });

  setInterval(() => {
    const cam = Graph.camera();
    cameraInfo.textContent = `Camera: x=${cam.position.x.toFixed(1)}, y=${cam.position.y.toFixed(1)}, z=${cam.position.z.toFixed(1)} | up: (${cam.up.x.toFixed(2)}, ${cam.up.y.toFixed(2)}, ${cam.up.z.toFixed(2)})`;
  }, 500);

  loadGraphData(); // Initial load
});
