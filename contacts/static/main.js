function enableDelete() {
    var atLeastOneIsChecked = $('input[name="contact_id"]:checked').length > 0;
    if (atLeastOneIsChecked == true) {
        $("#delete_button").prop("disabled", false);
    } else {
        $("#delete_button").prop("disabled", "disabled");
    }
}