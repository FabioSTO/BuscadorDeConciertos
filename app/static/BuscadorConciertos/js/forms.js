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
  
$('#buscar').submit(function(event) {
    event.preventDefault();
    $.ajax({
      url: '{% url "buscar_artista" %}',
      type: 'POST',
      data: $('#buscar').serialize(),
      success: function(data) {
        $('#lista-artistas').html(data);  // actualiza el contenido del ul con los nuevos artistas encontrados
    }
  });
});

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




  
