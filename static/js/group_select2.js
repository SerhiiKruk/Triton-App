$(document).ready(function () {
        $('#id_group_id').select2({
            theme: "classic",
            ajax: {
                url: 'http://pyhedgehog.pythonanywhere.com/student/create/',
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
