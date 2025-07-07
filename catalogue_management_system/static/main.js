const apiUrl = 'http://localhost:5000/catalogues';

function loadCatalogues() {
  fetch(apiUrl)
    .then(res => res.json())
    .then(data => {
      const tbody = document.querySelector('#catalogueTable tbody');
      tbody.innerHTML = '';
      data.forEach(cat => {
        tbody.innerHTML += `
          <tr>
            <td>${cat.id}</td>
            <td>${cat.name}</td>
            <td>${cat.description}</td>
            <td>${new Date(cat.start_date).toISOString().slice(0,10)}</td>
            <td>${new Date(cat.end_date).toISOString().slice(0,10)}</td>
            <td>${cat.status}</td>
            <td>
              <button onclick="deleteCatalogue(${cat.id})">Delete</button>
            </td>
          </tr>`;
      });
    });
}

document.getElementById('catalogueForm').onsubmit = function(e) {
  e.preventDefault();
  const cat = {
    id: document.getElementById('id').value,
    name: document.getElementById('name').value,
    description: document.getElementById('description').value,
    start_date: document.getElementById('start_date').value,
    end_date: document.getElementById('end_date').value,
    status: document.getElementById('status').value
  };
  fetch(apiUrl, {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify(cat)
  }).then(() => {
    loadCatalogues();
    this.reset();
  }).catch(error => {
    console.error('Fetch failed:', error);
  });
};

function deleteCatalogue(id) {
  fetch(`${apiUrl}/${id}`, { method: 'DELETE' })
    .then(() => loadCatalogues());
}

// Initial load
loadCatalogues();
