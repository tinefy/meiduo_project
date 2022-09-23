let vm = new Vue(
    {
        el: '#app',
        delimiters: ['[[', ']]'],
        data: {
            username: getCookie('username'),
            carts: [],
            carts_initial: [],

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
                this.carts_initial = JSON.parse(JSON.stringify(carts));
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
            update_selected: function (index) {
                this.calculate_selected_total_and_amount();
            },
            check_sku_count: function (index) {
                if (this.carts[index].count > 5) {
                    this.carts[index].count = 5;
                } else if (this.carts[index].count < 1) {
                    this.carts[index].count = 1;
                }
                this.update_count();
            },
            sku_count_add: function (index) {
                if (this.carts[index].count < 5) {
                    this.carts[index].count++;
                }
                this.update_count();
            },
            sku_count_minus: function (index) {
                if (this.carts[index].count > 1) {
                    this.carts[index].count--;
                }
                this.update_count();
            },
            update_count: function () {
                let url = '/carts/';

            },
        },
        mounted: function () {
            this.initialize_carts_data();
            this.calculate_total_count();
            this.calculate_selected_total_and_amount();
        },
        watch: {},
    }
)