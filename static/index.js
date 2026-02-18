document.getElementById('drop-area').addEventListener('click', () => {
    document.getElementById('file-input').click();
});

document.getElementById('file-input').addEventListener('change', (event) => {
    const file = event.target.files[0];
    if (file) {
        previewImage(file);
        clearPreviousOutput();
    }
});

document.addEventListener('paste', (event) => {
    const items = (event.clipboardData || event.originalEvent.clipboardData).items;
    for (const item of items) {
        if (item.kind === 'file') {
            const file = item.getAsFile();
            previewImage(file);
            clearPreviousOutput();
            break;
        }
    }
});

function previewImage(file) {
    const img = document.getElementById('preview');
    const reader = new FileReader();
    reader.onload = (event) => {
        img.src = event.target.result;
        img.style.display = 'block';
    };
    reader.readAsDataURL(file);
}

function clearPreviousOutput() {
    const resultSection = document.getElementById('result-section');
    if (resultSection) {
        resultSection.remove();
    }
}

document.addEventListener("DOMContentLoaded", function () {
    const toggleBtn = document.getElementById("toggle-btn");
    const infoBox = document.getElementById("extra-info");

    if (toggleBtn && infoBox) {
        toggleBtn.addEventListener("click", () => {
            if (infoBox.style.display === "none") {
                infoBox.style.display = "block";
                toggleBtn.innerText = "Hide Disease Info and Medicine";
            } else {
                infoBox.style.display = "none";
                toggleBtn.innerText = "Show Disease Info and Medicine";
            }
        });
    }
});
