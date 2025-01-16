// staff.js

let currentUserId = null;

// Открыть модальное окно для удаления пользователя
function openDeleteUserModal(userId) {
    currentUserId = userId;
    document.getElementById('deleteUserModal').style.display = 'flex';
}

// Открыть модальное окно для добавления пользователя
function openAddUserModal() {
    document.getElementById('addUserModal').style.display = 'flex';
}

// Закрыть модальное окно
function closeModal() {
    document.getElementById('deleteUserModal').style.display = 'none';
    document.getElementById('addUserModal').style.display = 'none';
}

// Подтвердить удаление пользователя
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

// Обработка формы добавления пользователя
document.getElementById('addUserForm').addEventListener('submit', function (event) {
    event.preventDefault();
    const formData = new FormData(this);
    const data = {
        user_id: formData.get('user_id'),
        password: formData.get('password'),
        permission_lvl: formData.get('permission_lvl')
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
