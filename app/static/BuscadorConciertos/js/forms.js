$(document).ready(function() {
  $(document).on('click', '.delete-button', function(event) {
    event.preventDefault();
    var form = $(this).closest('form');
    var url = form.attr('action'); 
    $.ajax({
      url: url,
      method: 'POST',
      data: form.serialize(),
      success: function(data) {
        form.closest('li').remove();
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
      $('#nombre').val('');
      $('#spinner').removeClass('show-spinner');
      $('#overlay').removeClass('overlay-show');
      if (data.includes('Duplicado')) {
        $('#nombre').addClass('error-input').attr('placeholder', '¡Artista duplicado!');
      }
      else if (data.includes('Inválido')) {
        $('#nombre').addClass('error-input').attr('placeholder', '¡Artista inválido!');
      } else {
        $('#nombre').removeClass('error-input');
        ensLista();}
      } 
  });
});

$(document).ready(function() {
  $('#nombre').on('click', function() {
    $(this).removeClass('error-input').attr('placeholder', 'Buscar artista');
  });
});


function ensLista() {
  var csrftoken = getCookie('csrftoken'); // Obtiene el valor del token CSRF de la cookie

  $.ajax({
    url: '/showLista/',
    type: 'GET',
    success: function(data) {
      $('#lista_artistas').empty();
      for (var i = 0; i < data.artists.length; i++) {
        var artist = data.artists[i];
        var listItem = '<li>' +
          artist.name;

        if (artist.is_spotified) {
          listItem += '<img src="/static/BuscadorConciertos/img/spotilogo.png" alt="Logo de Spotify">';
        }

        listItem += '<form id="delete-form-' + artist.id + '" method="post" action="/delete/' + artist.id + '/">' +
          '<input type="hidden" name="csrfmiddlewaretoken" value="' + csrftoken + '">' +
          '<button type="submit" class="delete-button" id="boton_borrar">Eliminar</button>' +
          '</form>' +
          '</li>';

        $('#lista_artistas').append(listItem);
      }
    }
  });
}

// Función auxiliar para obtener el valor del token CSRF de la cookie
function getCookie(name) {
  var cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    var cookies = document.cookie.split(';');
    for (var i = 0; i < cookies.length; i++) {
      var cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

$('#formArtista').on('reset', function() {
  $('#nombre').val(''); // Vacía el campo de texto al restablecer el formulario
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




  
