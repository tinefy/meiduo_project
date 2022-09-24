let vm = new Vue(
    {
        el: '#app',
        delimiters: ['[[', ']]'],
        data: {
            username: getCookie('username'),

            current_site:'',
            payment_amount:'',
        },
    }
)