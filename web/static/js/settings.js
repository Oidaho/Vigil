function saveSettings(currentPeerId) {
    const updated_settings = [];

    document.querySelectorAll('.setting-input').forEach(element => {
        const key = element.id;
        const currentValue = element.value;
        const originalValue = element.getAttribute('data-original-value');

        if (currentValue !== originalValue) {
            updated_settings.push({ key, value: currentValue });
        }
    });

    if (updated_settings.length > 0) {
        fetch(`/peers/${currentPeerId}/settings`, {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(updated_settings),
        })
        .then(response => {
            if (response.ok) {
                location.reload();
            } else {
                alert("Ошибка при сохранении настроек.");
            }
        })
        .catch(error => {
            console.error("Ошибка:", error);
        });
    }
}



function updateSelectBorder(selectElement) {
    selectElement.classList.remove('border-success', 'border-danger');
    const selectedValue = selectElement.value.toLowerCase();

    if (selectedValue === 'active' || selectedValue === 'allowed') {
        selectElement.classList.add('border-success');
    } else if (selectedValue === 'inactive' || selectedValue === 'disallowed') {
        selectElement.classList.add('border-danger');
    }
}

document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('.setting-input').forEach(selectElement => {
        updateSelectBorder(selectElement);
    });
});