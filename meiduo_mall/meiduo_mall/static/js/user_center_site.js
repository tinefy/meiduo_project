let vm = new Vue(
    {
        el: '#app',
        delimiters: ['[[', ']]'],
        data: {
            username: getCookie('username'),
            form_address: {
                receiver: '',
                province_id: '',
                city_id: '',
                district_id: '',
                place: '',
                mobile: '',
                tel: '',
                email: '',
            },
            provinces: [],
            cities: [],
            districts: [],
            is_show_editor: false,
        },
        methods: {
            show_editor: function (e) {
                e.preventDefault();
                this.is_show_editor = true;
            },
            close_editor: function (e) {
                e.preventDefault();
                this.is_show_editor = false;
            },
            get_provinces: function () {

            },
        },
        watch: {}
    }
)