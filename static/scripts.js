
$(document).ready(function () {
    $("#placesSearch").on("keyup", function () {
        var value = $(this).val().toLowerCase();
        $("#placesList li").filter(function () {
            $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
        });
    });
});

$(document).ready(function () {
    $('#objTable').DataTable({
        info: false,
        // "scrollY": document.documentElement.scrollHeight.toString() + 'px',
        // "scrollCollapse": true,
        lengthMenu: [
            [10, 25, 50, -1],
            [10, 25, 50, 'Все'],
        ],
        "autoWidth": false,
        'language': {
            "decimal": "",
            "emptyTable": "Нет данных",
            "thousands": ",",
            "lengthMenu": "Показать: _MENU_",
            "loadingRecords": "Загрузка...",
            "processing": "",
            "search": "Поиск объекта:",
            "zeroRecords": "По данному запросу ничего не найдено",
            "paginate": {
                "first": "Начало",
                "last": "Конец",
                "next": "След.",
                "previous": "Пред."
            }
        }
    });
});

