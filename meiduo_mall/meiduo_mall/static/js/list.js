let vm = new Vue(
    {
        el: '#app',
        delimiters: ['[[', ']]'],
        data: {
            username: getCookie('username'),

            carts: [],
            carts_total_count: 0,

            category_id: category_id,
            hot_skus: [],
        },
        methods: {
            get_hot_skus: function () {
                if (this.category_id) {
                    let url = '/list/hot/' + this.category_id + '/';
                    axios.get(
                        url, {responseType: 'json'}
                    ).then(
                        response => {
                            this.hot_skus = response.data.hot_skus;
                            for (let i = 0; i < this.hot_skus.length; i++) {
                                this.hot_skus[i].url = '/detail/' + this.hot_skus[i].id + '/';
                            }
                        }
                    ).catch(
                        error => {
                            console.log(error.response);
                        }
                    )
                }
            },
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
            this.get_hot_skus();
            this.get_carts();
        },
    }
)