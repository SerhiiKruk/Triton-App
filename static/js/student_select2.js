$(document).ready(function () {
        $('#id_student').select2({
            theme: "classic",
            ajax: {
                url: 'http://hedgehog94.pythonanywhere.com/add_profile/',
                delay: 500,
                dataType: 'json',
                processResults: function (data) {
                    return {
                        results: $.map(data, function (item) {
                            return {id: item.id, text: item.second_name};
                        })
                    };
                }
            },
            minimumInputLength: 3
        });
});
