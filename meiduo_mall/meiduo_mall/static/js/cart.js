let vm = new Vue(
    {
        el: '#app',
        delimiters: ['[[', ']]'],
        data: {
            username: getCookie('username'),
            carts: [],
            carts_temp: [],

            total_count: 0,
            total_selected_count: 1,
            total_selected_amount: 1,
            aaa: 100,
        },
        methods: {
            // 初始化购物车数据
            initialize_carts_data: function () {
                this.carts = JSON.parse(JSON.stringify(carts));
                for (let index in this.carts) {
                    this.carts[index].selected = this.carts[index].selected === 'True';
                }
                // 手动记录购物车的初始值，用于更新购物车失败时还原商品数量
                this.carts_temp = JSON.parse(JSON.stringify(carts));
            },
            calculate_total_count: function () {
                this.total_count = 0;
                for (let index in this.carts) {
                    this.total_count += this.carts[index].count;
                }
            },
            calculate_selected_total_and_amount: function () {
                this.total_selected_count = 0;
                this.total_selected_amount = 0;
                for (let index in this.carts) {
                    if (this.carts[index].selected) {
                        this.total_selected_count += this.carts[index].count;
                        this.total_selected_amount += this.carts[index].count * this.carts[index].price;
                    }
                }
                this.total_selected_amount = this.total_selected_amount.toFixed(2);
            },
            check_sku_count: function (index) {
                let count = 0;
                if (this.carts[index].count > 5) {
                    count = 5;
                } else if (this.carts[index].count < 1) {
                    count = 1;
                } else {
                    count = this.carts[index].count;
                }
                this.update_count(index, count);
            },
            sku_count_add: function (index) {
                let count = 0;
                if (this.carts[index].count < 5) {
                    count = this.carts[index].count + 1;
                } else {
                    count = 5;
                }
                this.update_count(index, count);
            },
            sku_count_minus: function (index) {
                let count = 0;
                if (this.carts[index].count > 1) {
                    count = this.carts[index].count - 1;
                } else {
                    count = 1;
                }
                this.update_count(index, count);
            },
            update_count: function (index, count) {
                let url = '/carts/';
                axios.put(
                    url, {
                        sku_id: this.carts[index].id,
                        count: count,
                        selected: this.carts[index].selected,
                    }, {
                        headers: {
                            'X-CSRFToken': getCookie('csrftoken')
                        },
                        responseType: 'json',
                        // withCredentials: true,
                    }
                ).then(
                    response => {
                        if (response.data.code === '0') {
                            this.carts[index].count = response.data.cart_sku.count;
                            this.calculate_total_count();
                            this.calculate_selected_total_and_amount();
                            this.carts_temp = $.extend(true, {}, this.carts);
                        } else {
                            alert(response.data.errmsg);
                            this.carts[index].count = this.carts_temp[index].count;
                        }
                    }
                ).catch(
                    error => {
                        console.log(error.response);
                        this.carts[index].count = this.carts_temp[index].count;
                    }
                )
            },
            update_selected: function (index) {
                let url = '/carts/';
                axios.put(
                    url, {
                        sku_id: this.carts[index].id,
                        count: this.carts[index].count,
                        selected: this.carts[index].selected,
                    }, {
                        headers: {
                            'X-CSRFToken': getCookie('csrftoken')
                        },
                        responseType: 'json',
                        // withCredentials: true,
                    }
                ).then(
                    response => {
                        if (response.data.code === '0') {
                            // this.carts[index].selected = response.data.cart_sku.selected;
                            this.calculate_selected_total_and_amount();
                            this.carts_temp = $.extend(true, {}, this.carts);
                        } else {
                            alert(response.data.errmsg);
                            this.carts[index].selected = this.carts_temp[index].selected;
                        }
                    }
                ).catch(
                    error => {
                        console.log(error.response);
                        this.carts[index].selected = this.carts_temp[index].selected;
                    }
                )
            },
            delete_goods: function (index) {
                let url = '/carts/';
                axios.delete(
                    url, {
                        data: {
                            sku_id: this.carts[index].id,
                        },
                        headers: {
                            'X-CSRFToken': getCookie('csrftoken')
                        },
                        responseType: 'json',
                        // withCredentials: true,
                    }
                ).then(
                    response => {
                        if (response.data.code === '0') {
                            this.carts.splice(index, 1);
                            this.calculate_total_count();
                            this.calculate_selected_total_and_amount();
                            this.carts_temp = $.extend(true, {}, this.carts);
                        } else {
                            alert(response.data.errmsg);
                        }
                    }
                ).catch(
                    error => {
                        console.log(error.response);
                    }
                )
            },
            select_all: function () {
                let selected = !this.select_all_status;

                let url = '/carts/selectall/';
                axios.put(
                    url, {
                        sku_id: this.carts[index].id,
                        count: this.carts[index].count,
                        selected: this.carts[index].selected,
                    }, {
                        headers: {
                            'X-CSRFToken': getCookie('csrftoken')
                        },
                        responseType: 'json',
                        // withCredentials: true,
                    }
                ).then(
                    response => {
                        if (response.data.code === '0') {
                            for (let index in this.carts) {
                                this.carts[index].selected = selected;
                            }
                            this.calculate_selected_total_and_amount();
                            this.carts_temp = $.extend(true, {}, this.carts);
                        } else {
                            alert(response.data.errmsg);
                            this.carts[index].selected = this.carts_temp[index].selected;
                        }
                    }
                ).catch(
                    error => {
                        console.log(error.response);
                        this.carts[index].selected = this.carts_temp[index].selected;
                    }
                )
            },
        },
        mounted: function () {
            this.initialize_carts_data();
            this.calculate_total_count();
            this.calculate_selected_total_and_amount();
        },
        computed: {
            select_all_status: {
                get: function () {
                    let selected = true;
                    for (let index in this.carts) {
                        if (this.carts[index].selected === false) {
                            selected = false;
                            break;
                        }
                    }
                    return selected;
                },
                // 解决 [Vue warn]: Computed property "xxx" was assigned to but it has no setter.
                set: function () {
                },
            },
        },
    }
)