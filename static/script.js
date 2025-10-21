const apiBase = '/';  // Same origin

async function addUser() {
    const name = document.getElementById('name').value;
    const email = document.getElementById('email').value;
    if (!name || !email) { alert("Enter name and email"); return; }

    const response = await fetch('/register_bulk', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify([{name, email}])
    });
    const data = await response.json();
    alert(JSON.stringify(data));
    document.getElementById('name').value = '';
    document.getElementById('email').value = '';
    getUsers();
}

async function getUsers() {
    const response = await fetch('/users');
    const users = await response.json();

    const tbody = document.querySelector('#userTable tbody');
    tbody.innerHTML = '';
    if (users.length === 0) {
        tbody.innerHTML = `<tr><td colspan="4" class="text-center">No users found</td></tr>`;
        return;
    }

    users.forEach(user => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td>${user.id}</td>
            <td><input type="text" value="${user.name}" id="name_${user.id}" class="form-control"></td>
            <td><input type="email" value="${user.email}" id="email_${user.id}" class="form-control"></td>
            <td>
                <button class="btn btn-success btn-sm me-1" onclick="updateUser(${user.id})">Update</button>
                <button class="btn btn-danger btn-sm" onclick="deleteUser(${user.id})">Delete</button>
            </td>
        `;
        tbody.appendChild(tr);
    });
}

async function updateUser(id) {
    const name = document.getElementById(`name_${id}`).value;
    const email = document.getElementById(`email_${id}`).value;

    const response = await fetch(`/update_user/${id}`, {
        method: 'PUT',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({name, email})
    });
    const data = await response.json();
    alert(JSON.stringify(data));
    getUsers();
}

async function deleteUser(id) {
    if (!confirm("Are you sure you want to delete this user?")) return;

    const response = await fetch(`/delete_user/${id}`, { method: 'DELETE' });
    const data = await response.json();
    alert(JSON.stringify(data));
}

// Load users on page load
window.onload = getUsers;

