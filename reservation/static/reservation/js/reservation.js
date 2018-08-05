$(function () {

    $('#reservation-table').DataTable();

    var loadForm = function () {
        var btn = $(this);
        $.ajax({
            url: btn.attr("data-url"),
            type: 'get',
            dataType: 'json',
            beforeSend: function () {
                $("#modal-reservation").modal("show");
            },
            success: function (data) {
                $("#modal-reservation .modal-content").html(data.html_form);
            }
        });
    };

    var saveForm = function () {
        var form = $(this);
        $.ajax({
            url: form.attr("action"),
            data: form.serialize(),
            type: form.attr("method"),
            dataType: 'json',
            success: function (data) {
                if (data.form_is_valid) {
                    $("#reservation-table tbody").html(data.html_reservation_list);  // <-- Replace the table body
                    $("#modal-reservation").modal("hide");
                }
                else {
                    $("#modal-reservation .modal-content").html(data.html_form);
                }
            }
        });
        return false;
    };

    $(".js-create-reservation").click(loadForm);
    $("#modal-reservation").on("submit", ".js-reservation-create-form", saveForm);

    // Update reservation
    $("#reservation-table").on("click", ".js-update-reservation", loadForm);
    $("#modal-reservation").on("submit", ".js-reservation-update-form", saveForm);

    $("#reservation-table").on("click", ".js-delete-reservation", loadForm);
    $("#modal-reservation").on("submit", ".js-reservation-delete-form", saveForm);
});
