$(function () {

    $('#facility-table').DataTable();

    var loadForm = function () {
        var btn = $(this);
        $.ajax({
            url: btn.attr("data-url"),
            type: 'get',
            dataType: 'json',
            beforeSend: function () {
                $("#modal-facility").modal("show");
            },
            success: function (data) {
                $("#modal-facility .modal-content").html(data.html_form);
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
                    $("#facility-table tbody").html(data.html_facility_list);  // <-- Replace the table body
                    $("#modal-facility").modal("hide");
                }
                else {
                    $("#modal-facility .modal-content").html(data.html_form);
                }
            }
        });
        return false;
    };

    $(".js-create-facility").click(loadForm);
    $("#modal-facility").on("submit", ".js-facility-create-form", saveForm);

    // Update facility
    $("#facility-table").on("click", ".js-update-facility", loadForm);
    $("#modal-facility").on("submit", ".js-facility-update-form", saveForm);

    // Delete facility
    $("#facility-table").on("click", ".js-delete-facility", loadForm);
    $("#modal-facility").on("submit", ".js-facility-delete-form", saveForm);
});
