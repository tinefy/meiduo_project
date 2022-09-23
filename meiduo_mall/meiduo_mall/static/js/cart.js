let vm = new Vue(
    {
        el: '#app',
        delimiters: ['[[', ']]'],
        data: {
            username: getCookie('username'),
            carts: carts,

            total_count: 0,
            total_selected_count: 1,
            total_selected_amount: 1,
            aaa:100,
        },
        methods: {
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
                this.total_selected_amount=this.total_selected_amount.toFixed(2);
            },
            update_selected:function (index){
                this.calculate_selected_total_and_amount();
            },
            check_sku_count: function () {
                if (this.cart_sku.count > 5) {
                    this.sku_count = 5;
                } else if (this.cart_sku.count < 1) {
                    this.sku_count = 1;
                }
                this.update_count();
            },
            sku_count_add: function () {
                if (this.cart_sku.count < 5) {
                    this.cart_sku.count++;
                }
                this.update_count();
            },
            sku_count_minus: function () {
                if (this.cart_sku.count > 1) {
                    this.cart_sku.count--;
                }
                this.update_count();
            },
            update_count:function (){

            },
        },
        mounted: function () {
            this.calculate_total_count();
            this.calculate_selected_total_and_amount();
        },
        watch:{

        },
    }
)