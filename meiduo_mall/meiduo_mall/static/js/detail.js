let vm = new Vue(
    {
        el: '#app',
        delimiters: ['[[', ']]'],
        data: {
            username: getCookie('username'),

            category_id: category_id,
        },
        methods: {

        },
    }
)