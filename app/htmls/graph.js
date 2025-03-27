import * as THREE from 'https://esm.sh/three';

// Entry point
fetch('data.json')
  .then(res => res.json())
  .then(initGraph)
  .catch(err => console.error('Error:', err));

function initGraph(gData) {
  const ARROW_SIZE = 6;
  const ARROW_COLOR = '#ffffff';
  const LINK_WIDTH = 0.5;
  const LINK_COLOR = '#ffffff';

  const Graph = new ForceGraph3D(document.getElementById('3d-graph'))
  .nodeThreeObject(createUMLNode)
  .nodeLabel(getNodeLabel)
  .linkLabel(getLinkLabel)
  .linkDirectionalArrowLength(ARROW_SIZE)
  .linkDirectionalArrowColor(ARROW_COLOR)
  .linkDirectionalArrowRelPos(1)
  .linkWidth(LINK_WIDTH)
  .linkColor(LINK_COLOR)
  .onNodeDragEnd(node => {
    node.fx = node.x; // lock x
    node.fy = node.y; // lock y
    node.fz = node.z; // lock z
  })
  .graphData(gData);

}

// Explicitly creates a UML-styled node
function createUMLNode(node) {
  const canvas = document.createElement('canvas');
  canvas.width = 480;
  canvas.height = 280;
  const ctx = canvas.getContext('2d');

  const marginLeft = 20;

  // Background
  ctx.fillStyle = 'white';
  ctx.fillRect(0, 0, canvas.width, canvas.height);

  ctx.strokeStyle = '#000';
  ctx.lineWidth = 4;
  ctx.strokeRect(0, 0, canvas.width, canvas.height);

  // Draw node name
  ctx.font = 'bold 24px Arial';
  ctx.fillStyle = '#000';
  ctx.textAlign = 'center';
  ctx.fillText(node.id, canvas.width / 2, 30);

  ctx.beginPath();
  ctx.moveTo(0, 40);
  ctx.lineTo(canvas.width, 40);
  ctx.stroke();

  let y = 60;

  if (node.type === 'module') {
    ctx.font = '20px Arial';
    ctx.fillStyle = '#007bff';
    ctx.textAlign = 'left';
    ctx.fillText(`Version: ${node.version || 'N/A'}`, marginLeft, y);
    y += 26;
    ctx.fillText(`Classes: ${(node.classes || []).length}`, marginLeft, y);
  }

  if (node.type === 'class') {
    ctx.textAlign = 'left';

    // Attributes
    ctx.font = '20px Arial';
    ctx.fillStyle = '#007bff';

    if (node.attributes) {
      node.attributes.forEach(attr => {
        ctx.fillText(attr, marginLeft, y);
        y += 26;
      });
    }

    // Methods
    ctx.fillStyle = '#e44c1a';
    if (node.methods) {
      y += 10;
      node.methods.forEach(method => {
        ctx.fillText(method, marginLeft, y);
        y += 26;
      });
    }
  }

  // Create 3D plane with this canvas texture
  const texture = new THREE.CanvasTexture(canvas);
  const material = new THREE.MeshBasicMaterial({
    map: texture,
    side: THREE.DoubleSide // ✨ render both front and back
  });
    const geometry = new THREE.PlaneGeometry(40, 20);
  return new THREE.Mesh(geometry, material);
}

// Node hover information explicitly formatted
function getNodeLabel(node) {
  return `
    <div>
      <b>${node.id}</b><br/>
      Type: ${node.type}<br/>
      ${node.methods ? `Methods: ${node.methods.length}<br/>` : ''}
      Lines of Code: ${node.linesOfCode || 'N/A'}<br/>
      ${node.version ? `Version: ${node.version}<br/>` : ''}
      ${node.module ? `Module: ${node.module}<br/>` : ''}
    </div>`;
}

// Link hover information explicitly formatted
function getLinkLabel(link) {
  return `
    <div>
      ${link.source.id} → ${link.target.id}<br/>
      Relation: ${link.relation}
    </div>`;
}

