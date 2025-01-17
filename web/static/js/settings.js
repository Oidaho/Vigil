function saveSettings() {
    const settingsData = [];

    document.querySelectorAll('.setting-input').forEach(element => {
        const key = element.id;
        const currentValue = element.value;
        const originalValue = element.getAttribute('data-original-value');

        if (currentValue !== originalValue) {
            settingsData.push({ key, value: currentValue });
        }
    });

    if (settingsData.length > 0) {
        fetch('/settings', {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(settingsData),
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('Настройки успешно сохранены!');
                document.querySelectorAll('.setting-input').forEach(element => {
                    const currentValue = element.value;
                    element.setAttribute('data-original-value', currentValue);
                });
            } else {
                alert('Ошибка при сохранении настроек.');
            }
        })
        .catch(error => {
            console.error('Ошибка:', error);
        });
    } else {
        alert('Нет изменений для сохранения.');
    }
}