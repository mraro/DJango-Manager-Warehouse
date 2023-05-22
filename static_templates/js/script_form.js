function previewImagem() {
    var imagem = document.querySelector('#id_img_pgm').files[0];
    var preview = document.querySelector('#preview');

    var reader = new FileReader();

    reader.onloadend = function () {
        preview.src = reader.result;
    }

    if (imagem) {
        reader.readAsDataURL(imagem);
    } else {
        preview.src = "";
    }
}
