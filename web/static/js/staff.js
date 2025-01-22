// staff.js

let currentUserId = null;

function openDeleteUserModal(userId) {
    currentUserId = userId;
    new bootstrap.Modal(document.getElementById('deleteUserModal')).show();
}

function openAddUserModal() {
    new bootstrap.Modal(document.getElementById('addUserModal')).show();
}

function closeModal() {
    new bootstrap.Modal(document.getElementById('deleteUserModal')).hide();
    new bootstrap.Modal(document.getElementById('addUserModal')).hide();
}

function confirmDelete() {
    if (currentUserId) {
        fetch(`/staff/${currentUserId}`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
            }
        })
        .then(response => {
            if (response.ok) {
                location.reload();
            } else {
                alert("An error occurred while deleting the staff member.");
            }
        })
        .catch(error => {
            console.error("Error:", error);
        });
    }
    closeModal();
}

function confirmAddUser() {
    const form = document.getElementById('addUserForm');
    const formData = new FormData(form);

    const data = {
        user_id: formData.get('user_id'),
        password: formData.get('password'),
        permission: formData.get('permission')
    };

    fetch(`/staff`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data)
    })
    .then(response => {
        if (response.ok) {
            location.reload();
        } else {
            alert("An error occurred while adding the staff member.");
        }
    })
    .catch(error => {
        console.error("Error:", error);
    });
}

