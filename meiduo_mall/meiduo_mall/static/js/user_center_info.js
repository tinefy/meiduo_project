let vm = new Vue(
    {
        el: '#app',
        delimiters: ['[[', ']]'],
        data: {
            // username: getCookie('username'),
            username: username,
            mobile: mobile,
            email: email,
            email_active: email_active,

            error_email: false,
            set_email: false,
            send_email_btn_disabled: false,
            send_email_tip: '重新发送验证邮件',

            browse_histories: []
        },
        methods: {
            check_email: function () {
                let re = /^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$/;
                if (re.test(this.email)) {
                    this.error_email = false;
                } else {
                    this.error_email = true;
                }
            },
            save_email: function () {
                this.check_email();
                if (!this.error_email) {
                    let url = '/emails/';
                    axios.put(
                        url, {
                            email: this.email
                        }, {
                            headers: {
                                'X-CSRFToken': getCookie('csrftoken')
                            },
                            responseType: 'json'
                        }
                    ).then(
                        response => {
                            if (response.data.code == '0') {
                                this.set_email = false;
                                this.send_email_tip = '已发送验证邮件';
                                this.send_email_btn_disabled = true;
                            } else if (response.data.code == '4101') {
                                location.href = '/login/?next=/info/';
                            } else {
                                alert(response.data.errmsg);
                            }
                        }
                    ).catch(
                        error => {
                            alert(error.response);
                        }
                    )
                }
            },
            cancel_email: function () {
                this.email = '';
                this.error_email = false;
            },
            get_browse_histories: function () {
                let url = '/browse_histories/';
                axios.get(
                    url, {responseType: 'json'}
                ).then(
                    response => {
                        this.browse_histories = response.data.skus;
                    }
                ).catch(
                    error => {
                        alert(error.response)
                    }
                )
            },
        },
        mounted: function () {
            this.email_active = (this.email_active == 'True') ? true : false;
            this.set_email = (this.email == '') ? true : false;
            this.get_browse_histories()
        },
    }
)