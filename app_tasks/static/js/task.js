if (window.djangoData) {
    const typeTaskData = window.djangoData.DictsTypeTask;

    document.addEventListener('DOMContentLoaded', () => {
        const selectElement = document.getElementById('type_task_id');
        const resultField = document.getElementById('department_id');

        selectElement.addEventListener('change', () => {
            const selectedKey = selectElement.value;
            if (selectedKey && typeTaskData.hasOwnProperty(selectedKey)) {
                const dict_type = typeTaskData[selectedKey];
                resultField.value = dict_type['department_id_id'];
            } else {
                resultField.value = '';
            }
        });
    });
} else {
    console.warn('window.djangoData не определен');
}