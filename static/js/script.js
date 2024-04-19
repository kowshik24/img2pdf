document.querySelector('.upload-area').addEventListener('click', () => {
    document.getElementById('file').click();
});

document.getElementById('file').addEventListener('change', handleFileSelect);

['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
    document.querySelector('.upload-area').addEventListener(eventName, function(e) {
        e.preventDefault();
        e.stopPropagation();
    }, false);
});

document.querySelector('.upload-area').addEventListener('drop', handleDrop);

function handleFileSelect(evt) {
    const files = evt.target.files;
    displayPreview(files);
}

function handleDrop(e) {
    const dt = e.dataTransfer;
    const files = dt.files;
    displayPreview(files);
    document.getElementById('file').files = files;
}

function displayPreview(files) {
    const preview = document.getElementById('preview');
    preview.innerHTML = '';

    Array.from(files).forEach(file => {
        if (!file.type.match('image.*')) {
            return;
        }

        const reader = new FileReader();
        reader.onload = (function(theFile) {
            return function(e) {
                const div = document.createElement('div');
                div.innerHTML = `<img class="thumb" src="${e.target.result}" title="${escape(theFile.name)}" style="width: 100px; height: auto;"/>`;
                preview.appendChild(div);
            };
        })(file);
        reader.readAsDataURL(file);
    });
}

document.getElementById('upload').addEventListener('click', function() {
    const files = document.getElementById('file').files;
    const formData = new FormData();

    for (let file of files) {
        formData.append('files[]', file, file.name);
    }

    fetch('/v1/upload', {
        method: 'POST',
        body: formData
    }).then(response => response.json())
    .then(result => {
        console.log('Server Response:', result.message);
    })
    .catch(error => {
        console.error('Error in file upload:', error);
    });
});

document.getElementById('convert').addEventListener('click', function() {
    fetch('/v1/convert_to_pdf')
    .then(response => response.blob())
    .then(blob => {
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.style.display = 'none';
        a.href = url;
        a.download = 'converted.pdf';
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
    })
    .catch(error => console.error('Error converting to PDF:', error));
});

document.getElementById('convert-white').addEventListener('click', function() {
    fetch('/v1/transform_to_white')
    .then(response => response.blob())
    .then(blob => {
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.style.display = 'none';
        a.href = url;
        a.download = 'white-background.pdf';
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
    })
    .catch(error => console.error('Error converting to white PDF:', error));
});
