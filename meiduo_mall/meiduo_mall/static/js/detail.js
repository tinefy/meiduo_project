let vm = new Vue(
    {
        el: '#app',
        delimiters: ['[[', ']]'],
        data: {
            username: getCookie('username'),

            hot_skus: [],

            category_id: category_id,
            sku_id: sku_id,
            sku_price: sku_price,
            sku_count: 1,
            sku_amount: sku_price,

            tab_content: {
                detail: true,
                pack: false,
                service: false,
                comment: false,
            }
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
            show_tab_content: function (tab) {
                let keys = Object.keys(this.tab_content);
                for (let index in keys) {
                    if (keys[index] === tab) {
                        this.tab_content[keys[index]] = true;
                    } else {
                        this.tab_content[keys[index]] = false;
                    }
                }
            },
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
            post_browse_history: function () {
                let url = '/browse_histories/';
                axios.post(
                    url, {
                        'sku_id': this.sku_id
                    }, {
                        headers: {
                            'X-CSRFToken': getCookie('csrftoken')
                        },
                        responseType: 'json'
                    }
                ).then(
                    response => {
                        console.log(response.data);
                    }
                ).catch(
                    error => {
                        console.log(error.response)
                    }
                )
            },
            post_visit_count: function () {
                let url = '/visit/' + this.category_id + '/';
                axios.post(
                    url, {}, {
                        headers: {
                            'X-CSRFToken': getCookie('csrftoken')
                        },
                        responseType: 'json'
                    }
                ).then(
                    response => {
                        console.log(response.data);
                    }
                ).catch(
                    error => {
                        console.log(error.response)
                    }
                )
            },
        },
        watch: {
            sku_count: {
                handler: function () {
                    this.sku_amount = (this.sku_count * this.sku_price).toFixed(2);
                },
                immediate: true,
            },
        },
        mounted: function () {
            this.get_hot_skus();
            this.post_browse_history();
            this.post_visit_count();
        },
    }
)