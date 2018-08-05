$(function () {

    var loadForm = function () {
        var btn = $(this);
        $.ajax({
            url: btn.attr("data-url"),
            type: 'get',
            dataType: 'json',
            beforeSend: function () {
                $("#modal-user-reservation").modal("show");
            },
            success: function (data) {
                $("#modal-user-reservation .modal-content").html(data.html_form);
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
                    $("#user-reservation-table tbody").html(data.html_user_reservation_list);  // <-- Replace the table body
                    $("#modal-user-reservation").modal("hide");
                }
                else {
                    $("#modal-user-reservation .modal-content").html(data.html_form);
                }
            }
        });
        return false;
    };

    $(".js-create-user-reservation").click(loadForm);
    $("#modal-user-reservation").on("submit", ".js-user-reservation-create-form", saveForm);

    // Update user-reservation
    $("#user-reservation-table").on("click", ".js-update-user-reservation", loadForm);
    $("#modal-user-reservation").on("submit", ".js-user-reservation-update-form", saveForm);

    $("#user-reservation-table").on("click", ".js-delete-user-reservation", loadForm);
    $("#modal-user-reservation").on("submit", ".js-user-reservation-delete-form", saveForm);
});
