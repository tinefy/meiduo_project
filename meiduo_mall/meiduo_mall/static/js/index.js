let vm = new Vue(
    {
        el: '#app',
        delimiters: ['[[', ']]'],
        data: {
            username: getCookie('username'),

            carts: [],
            carts_total_count: 0,

            floors: {
                f1_tabs: [
                    '时尚新品',
                    '畅想低价',
                    '手机配件',
                ],
                f2_tabs: [
                    '加价换购',
                    '畅享低价',
                ],
                f3_tabs: [
                    '生活用品',
                    '厨房用品',
                ],
                f1_tab: 1,
                f2_tab: 1,
                f3_tab: 1,
            },
        },
        methods: {
            get_carts: function () {
                let url = '/carts/simple/';
                axios.get(
                    url, {responseType: 'json'}
                ).then(
                    response => {
                        if (response.data.code === '0') {
                            this.carts = response.data.cart_skus;
                            this.carts_total_count = 0;
                            for (let index in this.carts) {
                                this.carts_total_count += this.carts[index].count;
                            }
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
        },
        mounted: function () {
            this.get_carts();
        },
    }
)