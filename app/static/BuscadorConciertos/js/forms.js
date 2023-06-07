$(document).ready(function() {
  $('.delete-button').click(function(event) {
    event.preventDefault(); // para que no se envíe el form
    var form = $(this).closest('form'); // encuentra el formulario más cercano al botón Eliminar
    var url = form.attr('action'); 
    $.ajax({
      url: url,
      method: 'POST', 
      data: form.serialize(),
      success: function(data) {
        form.closest('li').remove(); // elimina el elemento <li> correspondiente al artista de la lista
      }
    });
  });
});

$('#formArtista').submit(function(event) {
  event.preventDefault();
  var url = '/busqArtista/';
  $('#spinner').addClass('show-spinner');
  $('#overlay').addClass('overlay-show');
  $.ajax({
    url: url,
    type: 'POST',
    data: $(this).serialize(),
    success: function(data) {
      console.log('Artista enviado');
      showLista();
      $('#spinner').removeClass('show-spinner');
      $('#overlay').removeClass('overlay-show');
  }
});
});

function showLista() {
var url = '/showLista/';  // Reemplaza con la ruta correcta a tu vista que devuelve los artistas actualizados

$.ajax({
  url: url,
  type: 'GET',
  success: function(data) {
    $('#lista-artistas').html(data);// Actualiza el contenido del ulcon los nuevos artistas
  
  }
});
}

var prevScrollpos = window.pageYOffset;
var header = document.querySelector('.header');

window.addEventListener('scroll', function() {
var currentScrollPos = window.pageYOffset;

if (prevScrollpos > currentScrollPos) {
  header.style.transform = 'translateY(0)'; // Muestra banner
} else {
  header.style.transform = 'translateY(-100%)'; // Quita banner
}

prevScrollpos = currentScrollPos;
});




  
