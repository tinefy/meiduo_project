let vm = new Vue(
    {
        el: '#app',
        delimiters: ['[[', ']]'],
        data: {
            username: getCookie('username'),

            floors: {
                f1_tabs: [
                    '时尚新品',
                    '畅想低价',
                    '手机配件',
                ],
                f2_tabs: [
                    '加价换购',
                    '畅享低价',
                ],
                f3_tabs: [
                    '生活用品',
                    '厨房用品',
                ],
                f1_tab: 1,
                f2_tab: 1,
                f3_tab: 1,
            },
        },
    }
)