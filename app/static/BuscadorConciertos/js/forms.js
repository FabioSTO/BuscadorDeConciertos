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
  $('#spinner1').addClass('show-spinner1');
  $('#overlay').addClass('overlay-show');
  $.ajax({
    url: url,
    type: 'POST',
    data: $(this).serialize(),
    success: function(data) {
      console.log('Artista enviado');
      $('#nombre').val('');
      $('#spinner1').removeClass('show-spinner1');
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



// FOrmulario de conciertos

$(document).ready(function() {
  $('#filtros').submit(function(event) {
      event.preventDefault();
      var url = '/iniciarBusqueda/';
      $('#overlay2').addClass('overlay-show2');
      $('#spinner2').addClass('show-spinner2');
      $('#borrar_base').addClass('noShow');
      $('#diccionario').addClass('noShow');
      obtenerTitulares();
      $.ajax({
        url: url,
        type: 'POST',
        data: $(this).serialize(),
        success: function(data) {
          console.log(data);
          console.log('Filtrado');
          showConciertos(JSON.stringify(data));  // Lo necesito para que me funcione el JSON.parse
          loadMap(JSON.stringify(data));// Lo necesito para que me funcione el JSON.parse
          setTimeout(function() {
            $('#spinner2').removeClass('show-spinner2');
            $('#overlay2').removeClass('overlay-show2');
            $('#titulares').removeClass('titulares-show');  // Para darle tiempo a cargar el mapa
            $('#borrar_base').removeClass('noShow');
            $('#diccionario').removeClass('noShow');
          }, 2000);
      }
    });
  });
  });

  function obtenerTitulares() {
    $('#titulares').addClass('titulares-show');
    $.ajax({
      url: '/getTitulares/',
      type: 'GET',
      success: function(data) {
        console.log(data);
        var titularesDiv = $('#titulares');
        titularesDiv.empty();
        var randomIndex = Math.floor(Math.random() * data.length);
        var titularAleatorio = data[randomIndex];
        titularesDiv.append('<p>' + titularAleatorio + '</p>')
        //data.forEach(function(titular) {
        //  titularesDiv.append('<p>' + titular + '</p>');
        //});
      }
    });
  }
  
  function loadMap(conciertosJson) {
    var conciertos = JSON.parse(conciertosJson);
  
    var waypoints = "";
    var origin = "";
    var destination = "";
  
    for (var i = 1; i < conciertos.length - 1; i++) {
      waypoints += conciertos[i].place + "," + conciertos[i].country + "|";
    }
    origin = conciertos[0].place + "," + conciertos[0].country;
    destination = conciertos[conciertos.length - 1].place + "," + conciertos[conciertos.length - 1].country;

    console.log(waypoints);
    cred = 'AIzaSyC4GYQA9Yk5TpyJKIb4ATbasxQ9TIcpiaw'
  
    var maps_url = "https://www.google.com/maps/embed/v1/directions?key=" + cred + "&origin=" + origin + "&destination=" + destination + "&waypoints=" + waypoints.slice(0, -1) + "&units=metric&mode=driving";
  
    $('.map iframe').attr('src', maps_url);
  }

  function showConciertos(conciertosJson) {
    //console.log(conciertosJson);
    var diccionarioDiv = $('#diccionario');
    
    // Parseamos el JSON
    var conciertos = JSON.parse(conciertosJson);
  
    
    if (conciertos.length === 0) { // Si el diccionario está vacío
      diccionarioDiv.html('<p>No se encontraron conciertos.</p>');
      return;
    }
  
    var conciertosHtml = '<table id="tabla_conciertos"><tr><th>Nombre</th><th>Lugar</th><th>Fecha</th><th>Distancia</th><th>Precio</th></tr>'; // Para el enacbezado
  
  conciertos.forEach(function(concierto) {
    var fecha = new Date(concierto.date); // Convertir a fecha normal
    var fechaNormal = fecha.toDateString();
    var distkm = Math.round(concierto.distance/1000)
    conciertosHtml += '<tr><td>' + concierto.name + '</td><td>' + concierto.place + '</td><td>' + fechaNormal + '</td><td>' + distkm + " km" + '</td><td>' + " $" + concierto.price + '</td></tr>';
  });
  
  conciertosHtml += '</table>';
    diccionarioDiv.html(conciertosHtml);
  }
  

