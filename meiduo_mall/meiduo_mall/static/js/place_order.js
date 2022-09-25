let vm = new Vue(
    {
        el: '#app',
        delimiters: ['[[', ']]'],
        data: {
            username: getCookie('username'),

            current_site: default_address_id,
            pay_method: 2,
            payment_amount: payment_amount,

            order_submitting: false,
        },
        methods: {
            check_info: function () {
                if (!this.current_site) {
                    alert('请补充收货地址');
                    this.order_submitting = true;
                } else if (!this.pay_method) {
                    alert('请选择付款方式');
                    this.order_submitting = true;
                } else {
                    this.order_submitting = false;
                }
            },
            order_submit: function () {
                this.check_info();
                if (this.order_submitting === false) {
                    this.order_submitting = true;
                    let url = '/orders/commit/';
                    axios.post(
                        url, {
                            address_id: this.current_site,
                            pay_method: this.pay_method,
                        }, {
                            headers: {
                                'X-CSRFToken': getCookie('csrftoken')
                            },
                            responseType: 'json',
                        }
                    ).then(
                        response => {
                            this.order_submitting = false;
                            if (response.data.code === '0') {
                                location.href = '/orders/success/?order_id=' + response.data.order_id + '&payment_amount=' + this.payment_amount + '&pay_method=' + this.pay_method;
                            } else if (response.data.code === '4101') {
                                location.href = '/login/?next=/orders/settlement/';
                            } else {
                                alert(response.data.errmsg);
                            }
                        }
                    ).catch(
                        error => {
                            this.order_submitting = false;
                            console.log(error.response);
                        }
                    )
                }
            },
        },
    }
)