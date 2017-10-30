(function($) {
  "use strict"; // Start of use strict

  // Closes the sidebar menu
  $("#menu-close").click(function(e) {
    e.preventDefault();
    $("#sidebar-wrapper").toggleClass("active");
  });

  // Opens the sidebar menu
  $("#menu-toggle").click(function(e) {
    e.preventDefault();
    $("#sidebar-wrapper").toggleClass("active");
  });

  // Smooth scrolling using jQuery easing
  $('a.js-scroll-trigger[href*="#"]:not([href="#"])').click(function() {
    if (location.pathname.replace(/^\//, '') == this.pathname.replace(/^\//, '') && location.hostname == this.hostname) {
      var target = $(this.hash);
      target = target.length ? target : $('[name=' + this.hash.slice(1) + ']');
      if (target.length) {
        $('html, body').animate({
          scrollTop: target.offset().top
        }, 1000, "easeInOutExpo");
        return false;
      }
    }
  });

  // Closes responsive menu when a scroll trigger link is clicked
  $('.js-scroll-trigger').click(function() {
    $("#sidebar-wrapper").removeClass("active");
  });

    // Collapse Navbar
  var navbarCollapse = function() {
    if ($("#mainNav").offset().top > 100) {
      $("#mainNav").addClass("navbar-shrink");
    } else {
      $("#mainNav").removeClass("navbar-shrink");
    }
  };
  // Collapse now if page is not at top
  navbarCollapse();
  // Collapse the navbar when page is scrolled
  $(window).scroll(navbarCollapse);

  //#to-top button appears after scrolling
  var fixed = false;
  $(document).scroll(function() {
    if ($(this).scrollTop() > 250) {
      if (!fixed) {
        fixed = true;
        $('#to-top').show("slow", function() {
          $('#to-top').css({
            position: 'fixed',
            display: 'block'
          });
        });
      }
    } else {
      if (fixed) {
        fixed = false;
        $('#to-top').hide("slow", function() {
          $('#to-top').css({
            display: 'none'
          });
        });
      }
    }
  });

  $('button').click(function(e) {
    var estimate = $('#txtEstimate').val();
    $.ajax({
      url: '/estimate',
      data: $('form').serialize(),
      type: 'POST',
      success: function(response) {
        console.log(response.estimate);
        console.log(response.actual);
        $("#estimateTxt").text(response.estimate);
        $("#actualTxt").text(response.actual);
      },
      error: function(error) {
        console.log(error);
      },
      dataType: 'json'
    });
  });

  $('#linkForm').submit(function(e) {
    e.preventDefault();
    var estimate = $('#txtEstimate').val();
    $.ajax({
      url: '/estimate',
      data: $('form').serialize(),
      type: 'POST',
      success: function(response) {
        console.log(response.estimate);
        console.log(response.actual);
        $("#estimateTxt").text(response.estimate);
        $("#actualTxt").text(response.actual);
      },
      error: function(error) {
        console.log(error);
      },
      dataType: 'json'
    });
  });

})(jQuery); // End of use strict
