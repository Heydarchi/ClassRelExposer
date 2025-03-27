export function setupPanel(graphData) {
    const categorySelect = document.getElementById('categorySelect');
    const itemList = document.getElementById('itemList');
    const itemDetails = document.getElementById('itemDetails');
  
    function updateItemList(category) {
      itemList.innerHTML = '';
      const filtered = graphData.nodes.filter(node => node.type === category);
  
      filtered.forEach(node => {
        const li = document.createElement('li');
        li.textContent = node.id;
        li.addEventListener('click', () => showDetails(node));
        itemList.appendChild(li);
      });
    }
  
    function showDetails(node) {
      itemDetails.innerHTML = `
        <b>ID:</b> ${node.id}<br/>
        <b>Type:</b> ${node.type}<br/>
        ${node.module ? `<b>Module:</b> ${node.module}<br/>` : ''}
        ${node.version ? `<b>Version:</b> ${node.version}<br/>` : ''}
        ${node.attributes?.length ? `<b>Attributes:</b><ul>${node.attributes.map(a => `<li>${a}</li>`).join('')}</ul>` : ''}
        ${node.methods?.length ? `<b>Methods:</b><ul>${node.methods.map(m => `<li>${m}</li>`).join('')}</ul>` : ''}
      `;
    }
  
    // Initial population
    categorySelect.addEventListener('change', () => {
      updateItemList(categorySelect.value);
      itemDetails.innerHTML = 'Select an item to view details.';
    });
  
    updateItemList(categorySelect.value); // default load
  }
  