function navbarUpdate() {
  $.get("/db/stores/" + $("#search-store").val(), function(stores) {
    // Clear previous results
    $(".list-stores").empty()
    $(".stores-count").text(0)

    for (store of stores) {
      // Add stores buttons
      $("#" + store.type + "-stores").append(
        "<li><a id=\"" + store.id + "\" class=\"store-link my-1\" href=\"#\" ><h5>"+ store.name +"</h5></a></li>"
      );

      // Update number of stores badge per type
      $("#" + store.type + "-count").text(
        +$("#" + store.type + "-count").text() + 1
      );
    }
  });
}

$(document).ready(navbarUpdate);
$("#search-store").on("input", navbarUpdate);
