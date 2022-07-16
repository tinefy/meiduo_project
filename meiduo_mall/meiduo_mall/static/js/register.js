let vm = new Vue({
    el: '#app',
    delimiters: ['[[', ']]'],
    data: {
        username: 'mduser',
        password: 'mduser123',
        password2: 'mduser123',
        mobile: '13811723356',
        allow: 'true',

        error_name: false,
        error_password: false,
        error_password2: false,
        error_mobile: false,
        error_allow: false,
        error_submit: false,

        error_name_message: '',
        error_mobile_message: '',
    },
    methods: {
        check_username: function () {
            let re = /^[\w\d_-]{5,20}$/;
            if (re.test(this.username)) {
                this.error_name = false;
            } else {
                this.error_name = true;
                this.error_name_message = '请输入5-20个字符的用户名';
            }
        },
        check_password: function () {
            let re = /^[\w\d]{8,20}$/;
            if (re.test(this.password)) {
                this.error_password = false;
            } else {
                this.error_password = true;
            }
        },
        check_password2: function () {
            if (this.password2 == this.password2) {
                this.error_password2 = false;
            } else {
                this.error_password2 = true;
            }
        },
        check_mobile: function () {
            let re = /^1[3-9]\d{9}$/;
            if (re.test(this.mobile)) {
                this.error_mobile = false;
            } else {
                this.error_mobile = true;
                this.error_mobile_message = '您输入的手机号格式不正确';
            }
        },
        check_allow: function () {
            if (this.allow) {
                this.error_allow = false;
            } else {
                this.error_allow = true;
            }
        },
        on_submit: function (event) {
            // alert(event);
            this.check_username();
            this.check_password();
            this.check_password2();
            this.check_mobile();
            this.check_allow();
            if (this.error_name == true || this.error_password == true || this.error_password2 == true
                || this.error_mobile == true || this.error_allow == true) {
                this.error_submit = true;
                event.preventDefault();
            }
        },
    },
});