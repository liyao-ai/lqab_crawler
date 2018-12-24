$(function(){
  // 初始化方法
  init();
})

function init(){
    // 绑定按钮事件
    $("#search_button").bind("click",function(){
        doSearch();
    })
    // 绑定按键事件
    $("#keyword").bind("keyup",function(e){
        if(e.keyCode == 13){
            doSearch()
        }
        //alert(2);
    })

      // 绑定按键事件
    $("#search_remove_id").bind("keyup",function(){
        alert(3);
    })

}
// 请求数据
function doSearch(){
    var keyword = $("#keyword").val();
    var url = "/search/baidu/"+keyword;
    ajaxPost(url,null,successSearch,50000,errorSearch)
}
// 请求数据完成
function successSearch(result){
    var keyword = $("#keyword").val();
    if(result.length==0){

        var url = "/crawler/baidu/"+keyword;
        ajaxPost(url,null,successCrawler,50000,errorSearch)
        return ;
    }
    var  content =  $("#main_context").find("#ss").clone(false);
    content.attr("id","");
    content.css({"display":""});
    content.find("#table_title_id").html("关键字:<span style='color:red;'>"+keyword+"</span>");

    $.each(result,function(index,value){
        console.log(value);
        var item = content.find(".item:eq(0)").clone(false);
        item.css({"display":""});
        item.find(".item_a_a").text(value.title);
        item.find(".item_a_a").bind("click",function(){
            window.open(value.url);
        })
        item.find(".item_c").text(value.summary);
        item.find(".item_d").find("span").text("百度快照");
        item.find(".item_d").bind("click",function(){
            window.open( value.snapshot);
        })

        content.find("#show_table_id").find("#collapseTable").find(".row").append(item);
    })
    content.find("a").attr("href","#关键字"+keyword);
    content.find("#show_table_id").find("#collapseTable").attr("id","关键字"+keyword);

    $("#main_context").find("#ss").after(content);

    //console.log(result)
}
// 时时采集结果
function  successCrawler(result){
    if(result.code==1){
        doSearch()
    }
}

// 请求数据 失败
function errorSearch(result){
    alert(result.error_code)
}

// 清除文本内容
function clear(){
  $("#search_button").val("");
}