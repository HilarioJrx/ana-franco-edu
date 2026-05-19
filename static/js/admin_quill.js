document.addEventListener('DOMContentLoaded', function() {
    const textarea = document.getElementById('id_content');
    if (!textarea) return;

    // 1. Hide the original textarea
    textarea.style.display = 'none';

    // 2. Create the container for Quill
    const quillWrapper = document.createElement('div');
    quillWrapper.id = 'quill-editor';
    quillWrapper.style.height = '350px';
    quillWrapper.style.background = 'white';
    quillWrapper.style.color = 'black';
    quillWrapper.style.borderRadius = '0 0 8px 8px';
    quillWrapper.style.border = '1px solid #d1d5db';
    quillWrapper.style.borderTop = 'none';
    quillWrapper.style.fontFamily = 'inherit';

    // Apply some styles to the toolbar container when inserted
    const toolbarStyles = document.createElement('style');
    toolbarStyles.innerHTML = `
        .ql-toolbar.ql-snow {
            border: 1px solid #d1d5db !important;
            border-radius: 8px 8px 0 0 !important;
            background: #f9fafb !important;
        }
        .ql-container.ql-snow {
            border: 1px solid #d1d5db !important;
            border-radius: 0 0 8px 8px !important;
        }
        .ql-editor {
            font-size: 16px !important;
            line-height: 1.6 !important;
        }
    `;
    document.head.appendChild(toolbarStyles);

    // Insert Quill wrapper after the textarea
    textarea.parentNode.insertBefore(quillWrapper, textarea.nextSibling);

    // 3. Initialize Quill
    const quill = new Quill('#quill-editor', {
        theme: 'snow',
        modules: {
            toolbar: [
                [{ 'header': [1, 2, 3, false] }],
                ['bold', 'italic', 'underline', 'clean'],
                [{ 'list': 'ordered'}, { 'list': 'bullet' }],
                ['link']
            ]
        }
    });

    // 4. Load initial content from textarea
    quill.root.innerHTML = textarea.value;

    // 5. Sync Quill changes back to the textarea on form submission
    const form = textarea.closest('form');
    if (form) {
        form.addEventListener('submit', function() {
            // If Quill has only empty paragraphs, clear the content
            const html = quill.root.innerHTML;
            if (html === '<p><br></p>' || html === '<p></p>') {
                textarea.value = '';
            } else {
                textarea.value = html;
            }
        });
    }
});
