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
        mounted: function () {
            this.get_areas_data('province')
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
            get_areas_data: function (area) {
                if (area == 'province') {
                    let url = '/areas/';
                    this.provinces = this.get_areas(url).province_list
                } else if (area == 'city') {
                    let url = '/areas/?area_id=' + this.form_address.province_id;
                    this.cities = this.get_areas(url).sub_data.subs
                } else if (area == 'district') {
                    let url = '/areas/?area_id=' + this.form_address.city_id;
                    this.districts = this.get_areas(url).sub_data.subs
                }
            },
            get_areas: function (url) {
                let data_;
                axios.get(
                    url, {responseType: 'json'}
                ).then(
                    response => {
                        data_ = response.data;
                    }
                ).catch(
                    error => {
                        console.log(error.response);
                    }
                )
                return data_;
            },
        },
        watch: {
            'form_address.province_id': function () {
                this.get_areas_data('city')
            },
            'form_address.city_id': function () {
                this.get_areas_data('district')
            },
        },
    }
)