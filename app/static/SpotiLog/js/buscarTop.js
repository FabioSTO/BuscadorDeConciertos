$(document).ready(function() {
    $('#submitTop').on('click', function(e) {
        e.preventDefault();
        $('#buscarTop').submit();
    });

    $('#buscarTop').on('submit', function(e) {
        e.preventDefault();
        var url = '/SpotiLog/get_top_artists/';
        $('#spinner').addClass('show-spinner');
        $('#overlay').addClass('overlay-show');
        $.ajax({
            url: url,
            type: 'POST',
            data: $(this).serialize(),
            success: function() {
                showLista();
                $('#spinner').removeClass('show-spinner');
                $('#overlay').removeClass('overlay-show');
                console.log('Artistas guardados.');
            },
            error: function(xhr, status, error) {
                console.error(error);
            }
        });
    });
});
