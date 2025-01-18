let selectedUserId = null;

function openDeleteModal(userId) {
    selectedUserId = userId;
    new bootstrap.Modal(document.getElementById('deleteModal')).show();
}

function closeModal() {
    new bootstrap.Modal(document.getElementById('deleteModal')).hide();
}

function confirmDelete(currentPeerId) {
    if (selectedUserId) {
        fetch(`/peers/${currentPeerId}/queue/${selectedUserId}`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
            },
        })
        .then(response => {
            if (response.ok) {
                location.reload();
            } else {
                alert("An error occurred while deleting the message.");
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    }
    closeModal()
}