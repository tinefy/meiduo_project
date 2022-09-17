let vm = new Vue(
    {
        el: '#app',
        delimiters: ['[[', ']]'],
        data: {
            username: getCookie('username'),

            category_id: category_id,
            sku_price: sku_price,
        },
        methods: {

        },
    }
)