$(function () {
    $(".sidenav-collapse").sideNav();

    $(".sidenav-collapse").on('click', function () {
        $("#sidenav").toggleClass('collapsed'); // Toggle the 'collapsed' class
    });

    // Add event listener to handle window resize
    $(window).on('resize', function () {
        if ($(window).width() > 768) {
            // Remove 'collapsed' class when the screen size is larger than 768px
            $("#sidenav").removeClass('collapsed');
        }
    });
});
