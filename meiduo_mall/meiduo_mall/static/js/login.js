let vm = new Vue(
    {
        el: '#app',
        delimiters: ['[[', ']]'],
        data: {
            username: '',
            password: '',
            remembered: '',

            err_username: false,
            err_password: false,
        },
        methods: {
            check_username: function () {
                let re = /^[\w\d_-]{5,20}$/;

            },
            check_password: function () {
                let re = /^[\w\d]{8,20}$/;

            },
            on_submit:function (event){
                event.preventDefault()
            },
        },
    }
)