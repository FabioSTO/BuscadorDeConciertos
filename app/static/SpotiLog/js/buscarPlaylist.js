$(document).ready(function() {                          // Cuando se pulsa en la imagen de playlists
    $('#submitPlaylist').on('click', function(e) {
        e.preventDefault();
        $('#buscarPlaylist').submit();
    });

    $('#buscarPlaylist').on('submit', function(e) {
        e.preventDefault();
        var url = '/SpotiLog/get_playlists/';
        $.ajax({
            url: url,
            type: 'POST',
            data: $(this).serialize(),
            success: function(data) {
                
                $('#playlist_select').empty(); // Vaciamos previamente
        
                $('#playlist_select').append('<option value="">Selecciona una playlist</option>');
    
                for (var i = 0; i < data.length; i++) {
                    $('#playlist_select').append('<option value="' + data[i] + '">' + data[i] + '</option>');
                }
                $('#playlist_select').toggle();
            },
        });
    });
});

$(document).ready(function() {  // Para cuando se escoja una playlist
    $('#playlist_select').on('change', function() {
        var selectedOption = $(this).val();
        get_artists_from_playlist(selectedOption);
        ensLista();
    });
});

function get_artists_from_playlist(playlistName) {
    var url = '/SpotiLog/get_artists_from_playlist/';
    $('#spinner1').addClass('show-spinner1');
    $('#overlay').addClass('overlay-show');
    var csrftoken = getCookie('csrftoken'); // Obtén el valor del token CSRF de la cookie
    $.ajax({
        url: url,
        type: 'POST',
        data: {
            playlistName: playlistName, // Mandamos al views el nomnbre de la playlist seleccionada
            csrfmiddlewaretoken: csrftoken
        },
        success: function() {
            $('#spinner1').removeClass('show-spinner1');
            $('#overlay').removeClass('overlay-show');
            ensLista();
            console.log('Artistas guardados.');
        },
        error: function(xhr, status, error) {
            console.error(error);
        }
    });
}

function ensLista() {
    var csrftoken = getCookie('csrftoken'); // Obtiene el valor del token CSRF de la cookie
    var imagePath = "{% static 'SpotiLog/img/spotilogo.png' %}";
  
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