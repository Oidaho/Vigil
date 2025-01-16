let currentConversationId = null;

// Открыть модальное окно для удаления
function openDeleteModal(conversationId) {
    currentConversationId = conversationId;
    document.getElementById('deleteModal').style.display = 'flex';
}

// Закрыть модальное окно
function closeModal() {
    document.getElementById('deleteModal').style.display = 'none';
}

function confirmDelete() {
    if (currentConversationId) {
        fetch(`/conversations/${currentConversationId}`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
            },
        })
        .then(response => {
            if (response.ok) {
                location.reload(); // Перезагрузить страницу после удаления
            } else {
                alert("Ошибка при удалении беседы.");
            }
        })
        .catch(error => {
            console.error("Ошибка:", error);
        });
    }
    closeModal();
}

function saveSettings(conversationId) {
    const settings = [];
    const delays = [];

    const conversationContainer = document.getElementById(`conversation-${conversationId}`);

    conversationContainer.querySelectorAll('.form-check-input').forEach(input => {
        settings.push({
            id: input.id.replace('setting-', ''),
            is_enabled: input.checked ? 1 : 0,
        });
    });

    conversationContainer.querySelectorAll('.form-control').forEach(input => {
        delays.push({
            id: input.id.replace('delay-', ''),
            count: input.value,
        });
    });

    fetch(`/conversations/${conversationId}`, {
        method: 'PATCH',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ settings, delays }),
    })
    .then(response => {
        if (response.ok) {
            alert("Настройки успешно сохранены.");
            location.reload();
        } else {
            alert("Ошибка при сохранении настроек.");
        }
    })
    .catch(error => {
        console.error("Ошибка:", error);
    });
}