$(function () {

    var loadForm = function () {
        var btn = $(this);
        $.ajax({
            url: btn.attr("data-url"),
            type: 'get',
            dataType: 'json',
            beforeSend: function () {
                $("#modal-user-profile").modal("show");
            },
            success: function (data) {
                $("#modal-user-profile .modal-content").html(data.html_form);
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
                    $("#user-profile-table").html(data.html_user_profile_list);  // <-- Replace the table body
                    $("#modal-user-profile").modal("hide");
                }
                else {
                    $("#modal-user-profile .modal-content").html(data.html_form);
                }
            }
        });
        return false;
    };

    var saveForm2 = function () {
        var form = $(this);
        $.ajax({
            url: form.attr("action"),
            data: form.serialize(),
            type: form.attr("method"),
            dataType: 'json',
            success: function (data) {
                if (data.form_is_valid) {
                    document.location.href = '/'
                }
                else {
                    $("#modal-user-profile .modal-content").html(data.html_form);
                }
            }
        });
        return false;
    };

    // Update user-profile
    $(".js-update-user-profile").click(loadForm);
    $("#modal-user-profile").on("submit", ".js-user-profile-update-form", saveForm);

    $(".js-delete-user-profile").click(loadForm);
    $("#modal-user-profile").on("submit", ".js-user-profile-delete-form", saveForm2);
});
