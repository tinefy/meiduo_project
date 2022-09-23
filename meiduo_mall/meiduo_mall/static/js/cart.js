let vm = new Vue(
    {
        el: '#app',
        delimiters: ['[[', ']]'],
        data: {
            username: getCookie('username'),
            carts: carts,
        },
        methods: {},
    }
)