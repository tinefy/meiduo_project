let vm = new Vue(
    {
        el: '#app',
        delimiters: ['[[', ']]'],
        data: {
            username: getCookie('username'),

            f1_tabs: [
                '时尚新品',
                '畅想低价',
                '手机配件',
            ],

            f1_tab: 1,
            f2_tab: 1,
            f3_tab: 1,
        },
        methods: {
            floor_tab: function (tab_in_floor, index) {
                tab_in_floor = index + 1;
            },
        }
    }
)