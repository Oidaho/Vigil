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
                location.reload(); // Перезагрузить страницу после удаления
            } else {
                alert("Ошибка при удалении сотрудника.");
            }
        })
        .catch(error => {
            console.error("Ошибка:", error);
        });
    }
    closeModal();
}

document.getElementById('addUserForm').addEventListener('submit', function (event) {
    event.preventDefault();
    const formData = new FormData(this);
    const data = {
        user_id: formData.get('user_id'),
        password: formData.get('password'),
        permission: formData.get('permission')
    };

    fetch('/staff', {
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
            alert("Ошибка при добавлении сотрудника.");
        }
    })
    .catch(error => {
        console.error("Ошибка:", error);
    });
});
