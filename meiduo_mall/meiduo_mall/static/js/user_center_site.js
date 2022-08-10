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
            error_tips: {
                error_receiver: false,
                error_place: false,
                error_mobile: false,
                error_tel: false,
                error_email: false,
            },
            editing_address_index: -1,
        },
        methods: {
            clear_form_data: function () {
                let keys = Object.keys(this.form_address);
                for (let i = 0; i < keys.length; i++) {
                    this.form_address[keys[i]] = '';
                }
                this.clear_errors();
                this.get_areas('province');
            },
            clear_errors: function () {
                let keys = Object.keys(this.error_tips);
                for (let i = 0; i < keys.length; i++) {
                    this.error_tips[keys[i]] = '';
                }
            },
            show_editor: function (e) {
                e.preventDefault();
                this.is_show_editor = true;
            },
            close_editor: function (e) {
                e.preventDefault();
                this.is_show_editor = false;
            },
            get_areas: function (area) {
                // 注意：axios是异步执行的
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
                            this.form_address.province_id = this.provinces[0].id;
                            console.log(this.form_address.province_id);
                        } else if (area == 'city') {
                            this.cities = response.data.sub_data.subs;
                            this.form_address.city_id = this.cities[0].id;
                        } else if (area == 'district') {
                            this.districts = response.data.sub_data.subs;
                            this.form_address.district_id = this.districts[0].id;
                        }
                    }
                ).catch(
                    error => {
                        console.log(error.response);
                    }
                )
            },
            check_receiver: function () {
                let re = /^\s*?$/;
                if (re.test(this.form_address.receiver)) {
                    this.error_tips.error_receiver = true;
                } else {
                    this.error_tips.error_receiver = false;
                }
            },
            check_place: function () {
                let re = /^\s*?$/;
                if (re.test(this.form_address.place)) {
                    this.error_tips.error_place = true;
                } else {
                    this.error_tips.error_place = false;
                }
            },
            check_mobile: function () {
                let re = /^1[3-9]\d{9}$/;
                if (!re.test(this.form_address.mobile)) {
                    this.error_tips.error_mobile = true;
                } else {
                    this.error_tips.error_mobile = false;
                }
            },
            check_tel: function () {
                let re = /^(0[0-9]{2,3}-)?([2-9][0-9]{6,7})+(-[0-9]{1,4})?$/;
                if (!re.test(this.form_address.tel)) {
                    this.error_tips.error_tel = true;
                } else {
                    this.error_tips.error_tel = false;
                }
            },
            check_email: function () {
                let re = /^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$/;
                if (!re.test(this.form_address.email)) {
                    this.error_tips.error_email = true;
                } else {
                    this.error_tips.error_email = false;
                }
            },
            save_address: function (e, index = -1) {
                e.preventDefault()
                // if ()
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