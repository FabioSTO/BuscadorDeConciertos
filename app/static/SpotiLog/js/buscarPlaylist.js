$(document).ready(function() {
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