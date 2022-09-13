let vm = new Vue(
    {
        el: '#app',
        delimiters: ['[[', ']]'],
        data: {
            username: getCookie('username'),

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
        },
        mounted: function () {
            this.get_hot_skus();
        },
    }
)