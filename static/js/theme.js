$(".header--theme-button").on("click", function() {
    var primaryColor = $(this).css("--color1");
  
    $(".header--theme-button").removeClass("active");
    $(this).addClass("active");
  
    $(document.body).css("--color1", primaryColor);
  });

// Path: static\js\theme.js