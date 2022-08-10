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
            get_areas: function (area) {
                // 错误原因：axios是异步执行的，所以this.area_data还为空时就执行到下面了。
                let url = '';
                if (area == 'province') {
                    url = '/areas/';
                } else if (area == 'city') {
                    url = '/areas/?area_id=' + this.form_address.province_id;
                } else if (area == 'district') {
                    url = '/areas/?area_id=' + this.form_address.city_id;
                }
                axios.get(
                    url, {responseType: 'json'}
                ).then(
                    response => {
                        if (area == 'province') {
                            this.provinces = response.data.province_list;
                            // select下拉框设定默认值
                            this.form_address.province_id=this.provinces[0].id;
                            console.log(this.form_address.province_id);
                        } else if (area == 'city') {
                            this.cities = response.data.sub_data.subs;
                        } else if (area == 'district') {
                            this.districts = response.data.sub_data.subs;
                        }
                    }
                ).catch(
                    error => {
                        console.log(error.response);
                    }
                )
            },
        },
        watch: {
            'form_address.province_id': function () {
                this.get_areas('city');
            },
            'form_address.city_id': function () {
                this.get_areas('district');
            },
        },
        mounted: function () {
            this.get_areas('province')
        },
    }
)