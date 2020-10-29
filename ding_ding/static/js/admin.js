var currentStore;


// UPDATE

function updateSidebar() {
  let url = "/admin/panel/?q=" + $("#search-store").val();

  $("#stores").html(`
    <div class="spinner-border" role="status">
      <span class="sr-only align-middle">Loading...</span>
    </div>
  `)

  // ajax GET request
  $.get(url, function(response) {

    // Add stores buttons
    $('#stores').html(response);

    $(`[store-id=${currentStore}]`).addClass("active");

    // EVENTS

    // Switch "active" on button "Store"
    $(".store-link").on("click", function() {
      $(".store-link").removeClass("active");
      $(this).addClass("active");

      currentStore = $(this).attr('store-id')
      updateView();
    });

    // Switch "active" on button "Type"
    $(".type-link").on('click', function() {
      $(this).toggleClass("active");
    });
  });
}


function updateView() {
  let url = "/admin/store/" + currentStore;

  $("#admin").html(`
    <div class="spinner-border align-self-center" role="status">
      <span class="sr-only align-middle">Loading...</span>
    </div>
  `)

  // ajax GET request
  $.get(url, function(response) {
    $("#admin").html(response);

    // EVENTS
    $("#addItemForm").submit(addItem);
    $(".editItemForm").submit(editItem);
    $(".deleteItemButton").click(deleteItem);

    $(".editStoreForm").submit(editStore);
    $("#deleteStoreButton").click(deleteStore);
  });
}


// STORE

function addStore() {
  $("#addStoreButton").html("<span class=\"spinner-border spinner-border-sm\" role=\"status\" aria-hidden=\"true\"></span>");
  $("#addStoreButton").attr("disabled", "disabled");

  url = "/admin/add_store/";

  $.ajax({
    type: "POST",
    url: url,
    data: $(this).serialize(),
    success: function (data) {
      showSuccToast('Store added Successfully!');

      // Close menu and update page
      $("#addStore").modal('hide');
      updateSidebar();

      $("#addStoreButton").html("Add")
      $("#addStoreButton").removeAttr("disabled");
    },
    error: function (data) {
      showFailToast('Store is not added!', data.responseJSON.error);
    }
  });

  return false;
}


function editStore() {
  id = $(this).attr('store-id');

  $("#editStoreButton-" + id).html("<span class=\"spinner-border spinner-border-sm\" role=\"status\" aria-hidden=\"true\"></span>");
  $("#editStoreButton-" + id).attr("disabled", "disabled");

  url = "/admin/edit_store/";

  $.ajax({
    type: "POST",
    url: url,
    data: $(this).serialize(),
    success: function (data) {
      showSuccToast('Store edited successfully!');

      // Close menu and update page
      $("#editItem-" + id).modal('hide');
      $("#editItem-" + id).on('hidden.bs.modal', updateView);
    },
    error: function (data) {
      showFailToast('Store is not edited!', data.responseJSON.error);

      $("#editStoreButton-" + id).html("Edit");
      $("#editStoreButton-" + id).removeAttr("disabled");
    }
  });


  return false;
}


function deleteStore() {
  id = $(this).attr('store-id');

  $(this).html("<span class=\"spinner-border spinner-border-sm\" role=\"status\" aria-hidden=\"true\"></span>");
  $(this).attr("disabled", "disabled");

  $("#editStore-" + id).modal('hide');

  function funY() {
    $("#editStore-" + id).modal('show');

    url = "/admin/delete_store/";

    $.ajax({
      type: "POST",
      url: url,
      data: $("#editStoreForm-" + id).serialize(),
      success: function (data) {
        showSuccToast('Store deleted successfully!');

        // Close menu and update page
        // Horrible piece of shit
        $("#editStore-" + id).on('shown.bs.modal', function() {
          $("#editStore-" + id).modal('hide');
        });
        $("#editStore-" + id).modal('hide');

        $("#editStore-" + id).on('hidden.bs.modal', function() {
          $("#admin").empty();
          updateSidebar();
        });
      },
      error: function (data) {
        showFailToast('Store is not deleted!', data.responseJSON.error);
        $("#deleteStoreButton").html("Delete");
        $("#deleteStoreButton").removeAttr("disabled");
      }
    });
  }

  function funN() {
    $("#editStore-" + id).modal('show');
    showFailToast("Post in not deleted!");

    $("#deleteStoreButton").html("Delete");
    $("#deleteStoreButton").removeAttr("disabled");
  }

  confirmation(funY, funN);

  return false;
}


// ITEM

function addItem() {
  $("#addItemButton").html("<span class=\"spinner-border spinner-border-sm\" role=\"status\" aria-hidden=\"true\"></span>");
  $("#addItemButton").attr("disabled", "disabled");

  url = "/admin/add_item/";

  $.ajax({
    type: "POST",
    url: url,
    data: $(this).serialize(),
    success: function (data) {
      showSuccToast('Item added Successfully!');

      // Close menu and update page
      $("#addItem").modal('hide');
      $("#addItem").on('hidden.bs.modal', updateView);
    },
    error: function (data) {
      showFailToast('Item is not added!', data.responseJSON.error);

      $("#addItemButton").html("Add")
      $("#addItemButton").removeAttr("disabled");
    }
  });

  return false;
}


function editItem() {
  id = $(this).attr('item-id');

  $("#editItemButton-" + id).html("<span class=\"spinner-border spinner-border-sm\" role=\"status\" aria-hidden=\"true\"></span>");
  $("#editItemButton-" + id).attr("disabled", "disabled");

  url = "/admin/edit_item/";

  $.ajax({
    type: "POST",
    url: url,
    data: $(this).serialize(),
    success: function (data) {
      showSuccToast('Item edited Successfully!');

      // Close menu and update page
      $("#editItem-" + id).modal('hide');
      $("#editItem-" + id).on('hidden.bs.modal', updateView);
    },
    error: function (data) {
      showFailToast('Item is not edited!', data.responseJSON.error);

      $("#editItemButton-" + id).html("Edit")
      $("#editItemButton-" + id).removeAttr("disabled");
    }
  });

  return false;
}

function deleteItem() {
  id = $(this).attr('item-id');

  $(this).html("<span class=\"spinner-border spinner-border-sm\" role=\"status\" aria-hidden=\"true\"></span>");
  $(this).attr("disabled", "disabled");

  $("#editItem-" + id).modal('hide');

  function funY() {
    $("#editItem-" + id).modal('show');

    url = "/admin/delete_item/";

    $.ajax({
      type: "POST",
      url: url,
      data: $("#editItemForm-" + id).serialize(),
      success: function (data) {
        showSuccToast('Item deleted successfully!');

        // Close menu and update page
        // Horrible piece of shit
        $("#editItem-" + id).on('shown.bs.modal', function() {
          $("#editItem-" + id).modal('hide');
        });
        $("#editItem-" + id).modal('hide');
        $("#editItem-" + id).on('hidden.bs.modal', updateView);
      },
      error: function (data) {
        showFailToast('Item is not deleted!', data.responseJSON.error);

        $("#deleteItemButton" + id).html("Delete");
        $("#deleteItemButton" + id).removeAttr("disabled");
      }
    });
  }

  function funN() {
    $("#editItem-" + id).modal('show');
    showFailToast("Item is not deleted!");

    $("#deleteItemButton-" + id).html("Delete");
    $("#deleteItemButton-" + id).removeAttr("disabled");
  }

  confirmation(funY, funN);

  return false;
}


function showSuccToast(title) {
  $("#adminToastContainer").append(`
    <div class="toast success-toast bg-success p-1" data-delay="5000" aria-label="Close">
      <div class="toast-header bg-success text-light">
        <strong class="mr-auto">${title}</strong>
      </div>
    </div>
  `);
  $("#adminToastContainer .toast:last").toast('show');

  // Close toasts if clicked
  $(".toast").on('click', function() {
    $(this).toast('dispose');
  });
}


function showFailToast(title, msg="") {
  $("#adminToastContainer").append(`
    <div class="toast fail-toast bg-danger p-1" data-delay="5000" aria-label="Close">
      <div class="toast-header bg-danger text-light">
        <strong class="mr-auto">${title}</strong>
      </div>
      <div class="toast-body bg-danger text-light">${msg}</div>
    </div>
  `);
  $("#adminToastContainer .toast:last").toast('show');

  // Close toasts if clicked
  $(".toast").on('click', function() {
    $(this).toast('dispose');
  });
}


function confirmation(funY, funN) {
  $("#confirmation").modal('show');
  $("#confirmation input[name='password']").val(null);

  $("#confirmationForm").on('submit', function() {
    $.ajax({
      type: "POST",
      url: "/auth/confirm",
      data: $(this).serialize(),
      success: function() {
        $("#confirmation").modal('hide');
        funY();
      },
      error: function() {
        showFailToast("Wrong password!")
        $("#confirmation").modal('hide');
        funN();
      }
    });

    $("#confirmationForm").off('submit');

    return false;
  });

  $("#confirmationNo").on('click', function() {
    $("#confirmation").modal('hide');
    funN();
    $("#confirmationNo").off('click');
  });
}


// EVENTS

// Sidebar
$(document).ready(updateSidebar);
$("#search-store").on("input", updateSidebar);
$("#addStoreForm").on("submit", addStore);
