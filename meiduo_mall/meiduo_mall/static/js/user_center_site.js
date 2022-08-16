let vm = new Vue(
    {
        el: '#app',
        delimiters: ['[[', ']]'],
        data: {
            username: getCookie('username'),

            form_address: {
                receiver: '张三',
                province_id: '',
                city_id: '',
                district_id: '',
                place: '北京市东城区钱粮胡同 99 号',
                mobile: '13816769876',
                tel: '010-67678656',
                email: 'zhangsan@163.com',
            },
            form_address_edit: {
                province_id: '',
                city_id: '',
                district_id: '',
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
            editing_address_flag: false,

            addresses: JSON.parse(JSON.stringify(addresses)),
            // addresses: [{"title":"ABC",},],
            default_address_id: default_address_id == 'None' ? null : default_address_id,

            edit_title_index: null,
            new_title: '',
        },
        methods: {
            clear_form_data: function () {
                let keys = Object.keys(this.form_address);
                for (let i = 0; i < keys.length; i++) {
                    this.form_address[keys[i]] = '';
                }
                this.clear_errors();
                // this.get_areas('province');
            },
            clear_errors: function () {
                let keys = Object.keys(this.error_tips);
                for (let i = 0; i < keys.length; i++) {
                    this.error_tips[keys[i]] = '';
                }
            },
            show_editor: function (e, index = -1) {
                e.preventDefault();
                this.editing_address_index = index;

                if (index !== -1) {
                    this.editing_address_flag = true;
                    let t = JSON.parse(JSON.stringify(this.addresses[index]));
                    // 若直接赋值给form_address，因为没有province_id等，
                    // 会导致即使后续再添加province_id属性，也不会触发Vue Watch中的方法
                    let url = '/address/' + t.id + '/area/';
                    let address_area = {
                        province: t.province,
                        city: t.city,
                        district: t.district,
                    }
                    axios.get(
                        url, {responseType: 'json'}
                    ).then(
                        response => {
                            let address_area = response.data.address_area;
                            t.province_id = address_area.province_id;
                            t.city_id = address_area.city_id;
                            t.district_id = address_area.district_id;
                            this.clear_form_data();
                            // clear_form_data不能放在axios前面，
                            // 否则因为axios异步的原因，会导致clear_form_data时请求一次数据，
                            // 并将editing_address_flag置为false,
                            // 下面form_address赋值会再次引发请求数据并设置默认省市区
                            this.form_address = t
                            console.log('1' + this.form_address.city_id);
                        }
                    ).catch(
                        error => {
                            console.log(error.response);
                        }
                    )
                    console.log(this.form_address.city_id);
                    // for (let province of this.provinces) {
                    //     // console.log(province);
                    //     if (province.name === this.form_address.province) {
                    //         this.form_address.province_id = province.id;
                    //         console.log(this.form_address.province_id);
                    //     }
                    // }
                    // for (let city of this.cities) {
                    //     console.log(city);
                    //     if (city.name === this.form_address.city) {
                    //         this.form_address.city_id = city.id;
                    //         console.log(this.form_address.city_id);
                    //     }
                    // }
                    // for (let district of this.districts) {
                    //     // console.log(province);
                    //     if (district.name === this.form_address.district) {
                    //         this.form_address.district_id = district.id;
                    //         console.log(this.form_address.district_id);
                    //     }
                    // }
                    // this.get_areas('province');
                } else {
                    this.editing_address_flag = false;
                    this.clear_form_data();
                    // 清空form数据时，清空了省市区默认数据，会导致引发watch中获取市区数据的方法，
                    // 因为省市数据为空，发送的请求不正确，所以下方重新设置默认数据
                    this.form_address.province_id = this.provinces[0].id;
                    this.form_address.city_id = this.cities[0].id;
                    this.form_address.district_id = this.districts[0].id;
                }
                this.is_show_editor = true;
            },
            close_editor: function (e) {
                e.preventDefault();
                this.is_show_editor = false;
            },
            get_areas: function (area, set_default = true) {
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
                            if (response.data.code == '0') {
                                this.provinces = response.data.province_list;
                                // select下拉框设定默认值
                                if (set_default) {
                                    this.form_address.province_id = this.provinces[0].id;
                                }
                            } else {
                                console.log(response.data);
                                this.provinces = [];
                            }
                        } else if (area == 'city') {
                            if (response.data.code == '0') {
                                this.cities = response.data.sub_data.subs;
                                if (set_default) {
                                    this.form_address.city_id = this.cities[0].id;
                                }
                                console.log(this.form_address.city_id);
                            } else {
                                console.log(response.data);
                                this.cities = [];
                            }
                        } else if (area == 'district') {
                            if (response.data.code == '0') {
                                this.districts = response.data.sub_data.subs;
                                if (set_default) {
                                    this.form_address.district_id = this.districts[0].id;
                                }

                            } else {
                                console.log(response.data);
                                this.districts = [];
                            }
                        }
                    }
                ).catch(
                    error => {
                        console.log(error.response);
                        if (area == 'province') {
                            this.provinces = [];
                        } else if (area == 'city') {
                            this.cities = [];
                        } else if (area == 'district') {
                            this.districts = [];
                        }
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
            save_address: function (e) {
                e.preventDefault();
                this.check_receiver();
                this.check_place();
                this.check_mobile();

                let error_ = false;
                for (let item_ of Object.keys(this.error_tips)) {
                    if (this.error_tips[item_]) {
                        error_ = true;
                    }
                }
                if (error_) {
                    alert('信息填写有误！');
                    return;
                }
                if (this.editing_address_index === -1) {
                    let url = '/address/create/';
                    axios.post(
                        url, this.form_address, {
                            headers: {
                                'X-CSRFToken': getCookie('csrftoken')
                            },
                            responseType: 'json',
                        }
                    ).then(
                        response => {
                            if (response.data.code == '0') {
                                this.addresses.splice(0, 0, response.data.address);
                                this.is_show_editor = false;
                                this.clear_form_data();
                            } else if (response.data.code == '4101') {
                                location.href = '/login/?next=/address/';
                            } else {
                                alert(response.data.errmsg);
                            }
                        }
                    ).catch(
                        error => {
                            console.log(error.response);
                        }
                    )
                } else {
                    let url = '/address/' + this.addresses[this.editing_address_index].id + '/modify/';
                    // let form_address_ = $.extend(true, {}, this.form_address)
                    // form_address_[title] = this.addresses[this.editing_address_index].title;
                    axios.put(
                        url, this.form_address, {
                            headers: {
                                'X-CSRFToken': getCookie('csrftoken')
                            },
                            responseType: 'json',
                        }
                    ).then(
                        response => {
                            this.addresses[this.editing_address_index] = response.data.address;
                            this.is_show_editor = false;
                            this.clear_form_data();
                        }
                    ).catch(
                        error => {
                            console.log(error.response);
                        }
                    )
                }
            },
            save_title: function (index) {
                // e.preventDefault();
                this.edit_title_index;
            },
            cancel_title: function (index) {
                // e.preventDefault();
                this.new_title;
            },
            delete_address: function (index) {
                // e.preventDefault();
                this.new_title;
            },
            set_default: function (index) {
                // e.preventDefault();
                this.new_title;
            },
        },
        watch: {
            'form_address.province_id': function () {
                if (!this.editing_address_flag) {
                    this.get_areas('city');
                } else if (this.editing_address_flag) {
                    this.get_areas('city', false);
                    this.editing_address_flag = false;
                }
            },
            'form_address.city_id': function () {
                if (!this.editing_address_flag) {
                    this.get_areas('district');
                } else if (this.editing_address_flag) {
                    this.get_areas('district', false);
                    this.editing_address_flag = false;
                }
            },
        },
        mounted: function () {
            this.get_areas('province')
            console.log(this.addresses)
        },
    }
)