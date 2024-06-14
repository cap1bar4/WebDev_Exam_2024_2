
document.addEventListener('DOMContentLoaded', (event) => {
    const deleteModal = document.getElementById('deleteModal');
    deleteModal.addEventListener('show.bs.modal', (event) => {
        const button = event.relatedTarget;
        const bookId = button.getAttribute('data-book-id');
        const bookTitle = button.getAttribute('data-book-title');

        const modalTitle = deleteModal.querySelector('#bookTitle');
        const modalBookId = deleteModal.querySelector('#bookId');

        modalTitle.textContent = bookTitle;
        modalBookId.value = bookId;
    });
});
