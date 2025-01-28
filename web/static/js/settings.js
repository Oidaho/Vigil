function saveActiveTab(tabId) {
    localStorage.setItem('activeTab', tabId);
}

function loadActiveTab() {
    const activeTabId = localStorage.getItem('activeTab');
    if (activeTabId) {
        const tabTrigger = document.querySelector(`[href="${activeTabId}"]`);
        if (tabTrigger) {
            new bootstrap.Tab(tabTrigger).show();
        }
    }
}

document.addEventListener('DOMContentLoaded', function () {
    loadActiveTab();

    const tabLinks = document.querySelectorAll('.nav-pills .nav-link');
    tabLinks.forEach(link => {
        link.addEventListener('click', function (event) {
            const tabId = event.target.getAttribute('href');
            saveActiveTab(tabId);
        });
    });
});

let currentId = null;
let currentType = null;

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
        fetch(`/peers/${currentPeerId}/settings/`, {
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
                alert("An error occurred while saving the settings.");
            }
        })
        .catch(error => {
            console.error("Error:", error);
        });
    }
}


function updateSelectBorder(selectElement) {
    selectElement.classList.remove('border-success', 'border-danger', 'border-warning');
    const selectedValue = selectElement.value.toLowerCase();

    if (selectedValue === 'active' || selectedValue === 'allowed') {
        selectElement.classList.add('border-success');
    } else if (selectedValue === 'inactive' || selectedValue === 'disallowed') {
        selectElement.classList.add('border-danger');
    } else if (selectedValue === 'disallowed_quiet_delete' || selectedValue === 'active_quiet_delete') {
        selectElement.classList.add('border-warning');
    }
}

document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('.setting-input').forEach(selectElement => {
        updateSelectBorder(selectElement);
    });
});


function openDeleteModal(type, id) {
    currentId = id;
    currentType = type;
    new bootstrap.Modal(document.getElementById('deleteModal')).show();
}


function openAddLinkModal() {
    new bootstrap.Modal(document.getElementById('addLinkModal')).show();
}


function openAddHostModal() {
    new bootstrap.Modal(document.getElementById('addHostModal')).show();
}


function openAddWordModal() {
    new bootstrap.Modal(document.getElementById('addWordModal')).show();
}


function closeModal() {
    new bootstrap.Modal(document.getElementById('deleteModal')).hide();
    new bootstrap.Modal(document.getElementById('addLinkModal')).hide();
    new bootstrap.Modal(document.getElementById('addHostModal')).hide();
    new bootstrap.Modal(document.getElementById('addWordModal')).hide();
}


function confirmDelete(currentPeerId) {
    const endpoints = {
        "word": `/peers/${currentPeerId}/settings/words`,
        "link": `/peers/${currentPeerId}/settings/links`,
        "host": `/peers/${currentPeerId}/settings/hosts`,
    };

    if (currentId && currentType) {
        const endpoint = `${endpoints[currentType]}/${currentId}`;

        fetch(endpoint, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
            },
        })
        .then(response => {
            if (response.ok) {
                location.reload();
            } else {
                alert("An error occurred while deleting the item.");
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    }

    closeModal();
}


function addLink(currentPeerId) {
    const item_value = document.getElementById('linkValue').value;
    const endpoint = `/peers/${currentPeerId}/settings/links`;

    if (item_value) {
        fetch(endpoint, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(item_value),
        })
        .then(response => {
            if (response.ok) {
                location.reload();
            } else {
                alert("An error occurred while adding the link.");
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    }

    closeModal();
}


function addHost(currentPeerId) {
    const item_value = document.getElementById('hostValue').value;
    const endpoint = `/peers/${currentPeerId}/settings/hosts`;

    if (item_value) {
        fetch(endpoint, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(item_value),
        })
        .then(response => {
            if (response.ok) {
                location.reload();
            } else {
                alert("An error occurred while adding the domain.");
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    }

    closeModal();
}


function addWord(currentPeerId) {
    const item_value = document.getElementById('wordValue').value;
    const endpoint = `/peers/${currentPeerId}/settings/words`;

    if (item_value) {
        fetch(endpoint, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(item_value),
        })
        .then(response => {
            if (response.ok) {
                location.reload();
            } else {
                alert("An error occurred while adding the word.");
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    }

    closeModal();
}