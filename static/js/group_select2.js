$(document).ready(function () {
        $('#id_group_id').select2({
            theme: "classic",
            ajax: {
                url: 'http://127.0.0.1:1555/student/create/',
                delay: 500,
                dataType: 'json',
                processResults: function (data) {
                    return {
                        results: $.map(data, function (item) {
                            return {id: item.id, text: item.name};
                        })
                    };
                }
            },
            minimumInputLength: 3
        });
    });