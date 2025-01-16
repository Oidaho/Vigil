let selectedUserId = null;

function openDecrementModal(userId) {
    selectedUserId = userId;
    new bootstrap.Modal(document.getElementById('decrementModal')).show();
}

function openDeleteModal(userId) {
    selectedUserId = userId;
    new bootstrap.Modal(document.getElementById('deleteModal')).show();
}

function closeModal(userId) {
    new bootstrap.Modal(document.getElementById('deleteModal')).hide();
    new bootstrap.Modal(document.getElementById('decrementModal')).hide();
}

function confirmDecrement(currentPeerId) {
    if (selectedUserId) {
        fetch(`/peers/${currentPeerId}/sanctions/${selectedUserId}`, {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json',
            },
        })
        .then(response => {
            if (response.ok) {
                location.reload();
            } else {
                alert('Ошибка при уменьшении санкции');
            }
        })
        .catch(error => {
            console.error('Ошибка:', error);
        });
    }
    closeModal()
}

// Подтверждение удаления санкции
function confirmDelete(currentPeerId) {
    if (selectedUserId) {
        fetch(`/peers/${currentPeerId}/sanctions/${selectedUserId}`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
            },
        })
        .then(response => {
            if (response.ok) {
                location.reload();
            } else {
                alert('Ошибка при удалении санкции');
            }
        })
        .catch(error => {
            console.error('Ошибка:', error);
        });
    }
    closeModal()
}