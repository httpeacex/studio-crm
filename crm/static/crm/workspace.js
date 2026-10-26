document.addEventListener('keydown', (event) => {
  const editable = event.target.closest('input, textarea, select, [contenteditable="true"]');
  if (event.key === '/' && !editable && !event.ctrlKey && !event.metaKey && !event.altKey) {
    const search = document.getElementById('search');
    if (search) {
      event.preventDefault();
      search.focus();
    }
  }
});

document.querySelectorAll('.toolbar select, .toolbar input[type="checkbox"]').forEach((control) => {
  control.addEventListener('change', () => control.form.requestSubmit());
});
