if (window.djangoData) {
    const priorityData = window.djangoData.listOfDictsPriority;
    const typeTaskData = window.djangoData.listOfDictsTypeTask;


document.addEventListener('DOMContentLoaded', function() {
  const field1 = document.querySelector('type_task_id');
  const field2 = document.querySelector('department_id');

  if (field1 && field2) {
    field1.addEventListener('change', function() {
      const value = field1.value;
      for (let i = 0; i < priorityData.length; i++) {
        const item = priorityData[i];
        if const

}
      document.
      for
      if (value === 'X') {
        field2.value = 'Новое значение';
      }
      }
    });
  }
});

