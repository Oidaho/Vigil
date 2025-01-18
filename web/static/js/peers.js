let currentPeerId = null;

function openRemoveMarkModal(peerId) {
    currentPeerId = peerId;
    new bootstrap.Modal(document.getElementById('removeMarkModal')).show();
}

function closeModal() {
    new bootstrap.Modal(document.getElementById('removeMarkModal')).hide();
}

function confirmRemoveMark() {
    if (currentPeerId) {

        fetch(`/peers/${currentPeerId}`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
            }
        })
        .then(response => {
            if (response.ok) {
                location.reload();
            } else {
                alert("An error occurred while deleting the chat label.");
            }
        })
        .catch(error => {
            console.error("Error:", error);
        });
    }
    closeModal()
}