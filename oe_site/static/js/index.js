let record_on = false; // 给get_data()提供指示
let is_owner=false;

// 默认不显示拓展导航栏与数据页面
$(".extend").hide();
let is_extend = false;

// 默认显示测量页面
$(".page").hide()
$("#page_measurement").fadeIn(1000);

// 数据
load_data();

// 点击">"/"<"图标控制拓展导航栏的显示与关闭
$("#trigger").click(function () {
    is_extend = !is_extend;
    if (is_extend) {
        $(".extend").fadeIn(1000);
        $("#collapse").hide();
    } else {
        $(".extend").hide();
        $("#collapse").fadeIn(1000);
    }
})

// 通过导航栏, 在不同页面中切换
$("#switch_page_measurement").click(function () {
    $(".page").hide();
    $("#page_measurement").fadeIn(1000);
})
$("#switch_page_data").click(function () {
    $(".page").hide();
    $("#page_data").fadeIn(1000);
})

// 点击"start_record"按钮
$("#start_record").click(function () {
    if ( is_owner === false && record_on === false) {
        let suffix = exp_post.suffix.value;
        $.ajax({
            url: "exp_post",
            type: "post",
            async: false,
            data: {
                "flag": 1,
                "suffix": suffix
            },
            success: function (filename) {
                // 返回文件名, 留作拓展接口
                filename
            }
        })
        is_owner = true;
    }
})

// 点击"end_record"按钮
$("#end_record").click(function () {
    if( is_owner === true && record_on === true) {
        $.ajax({
            url: "exp_post",
            type: "post",
            async: false,
            data: {
                "flag": 2,
            },
            success: function () {
            }
        });
        is_owner = false;
    }
})

// $("#chart").click(function(){
//     load_data();
// })

// $$$ chart refresh interval

// 设定图的刷新间隔, 单位为ms
const interval = 500;
self.setInterval("load_data()",interval);


// 对数据展示做设置

// 将文件信息转为JSON方便JS使用
let files_json = JSON.parse($("#files_json")[0].textContent);
let files = files_json.files; // 得到的JS变量files为一个数组

// 在页面上显示文件详情
let files_info = $("#files_info")
init_files_table(); // 刷新表格

function init_files_table(){
    files_info.empty(); // 清空表格内容
    for (let file of files){
        var file_detail = get_file_detail(file);
        files_info.prepend(file_detail);
    }
}

function get_file_detail(file){
    var file_detail = ` <tr class="file_detail">
                            <!-- <td class="file_name">${file.name}</td> --!>
                            <td class="file_date">${file.format_date}</td>
                            <td class="file_note">${file.note}</td>
                            <td>
                                <a href="data/${file.url}">
                                    <svg class="icon" aria-hidden="true">
                                        <use xlink:href="#icon-down"></use>
                                    </svg>
                                </a>
                            <td>
                        </tr>`;
    return file_detail
}

// 排序功能
let file_table_heads = document.querySelectorAll("#file_table th:nth-child(-n+2)"); //对表头的前2个值做排序功能
for (let file_table_head of file_table_heads) {
    file_table_head.onclick = function () {
        // 全部重置为初始状态
        for (let file_table_head of file_table_heads) {
            if (file_table_head !== this) {
                file_table_head.className = "sort";
            }
        }
        // 现在是否是正序
        if (this.classList.contains("sort-asc")) { // 倒序排列
            this.className = "sort-desc";
            files.sort(compare(this.dataset.key, false)); // 对数据进行排序
            init_files_table();
        } else { // 正序排列
            this.className = "sort-asc";
            files.sort(compare(this.dataset.key, true)); // 对数据进行排序
            init_files_table();
        }
    }
}

// https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Reference/Global_Objects/Array/sort
// 用来指定按某种顺序进行排列的函数。如果省略，元素按照转换为的字符串的各个字符的Unicode位点进行排序。
function compare(key, sort) {
    
    return function (value1, value2) {
        let flag = 0;
        if (value1[key] > value2[key]) {
            flag = 1;
        } else if (value1[key] < value2[key]) {
            flag = -1;
        }
        return sort ? flag : flag * -1;
    }
}