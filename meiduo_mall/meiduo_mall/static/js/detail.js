let vm = new Vue(
    {
        el: '#app',
        delimiters: ['[[', ']]'],
        data: {
            username: getCookie('username'),

            category_id: category_id,
            sku_price: sku_price,
            sku_count: 1,

        },
        methods: {
            check_sku_count: function () {
                if (this.sku_count > 5) {
                    this.sku_count = 5;
                } else if (this.sku_count < 1) {
                    this.sku_count = 1;
                }
            },
            sku_count_add: function () {
                if (this.sku_count < 5) {
                    this.sku_count++;
                }
            },
            sku_count_minus: function () {
                if (this.sku_count > 1) {
                    this.sku_count--;
                }
            },
        },
    }
)