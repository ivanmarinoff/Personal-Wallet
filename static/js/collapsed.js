$(function() {
    // Check the window width

  $(".sidenav-collapse").on('click', function() {
    // Check the window width
    if ($(window).width() === 0) {
      // Hide the sidebar captions and text
      $("#sidenav ul").hide();

      // Show the side menu icons
      $("#sidenav ul li a i").show();
    } else {
      // Remove the 'collapsed' class to expand the side menu on small screens
      if ($(window).width() <= 700) {
        $("#sidenav").removeClass('collapsed');
      }
    }
  });
});