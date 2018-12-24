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

    if(result.length==0){
        var keyword = $("#keyword").val();
        var url = "/crawler/baidu/"+keyword;
        ajaxPost(url,null,successCrawler,50000,errorSearch)
        return ;
    }
    var  content =  $("#main_context");
	var list = content.find(".item");
    $.each(list,function(index,value){
        if(index>0){
            $(value).remove();
        }
    })
    $.each(result,function(index,value){
        console.log(value);
        var item = content.find(".item:eq(0)").clone(false);
        item.css({"display":""});
        item.find(".item_a_a").text(value[1]);
        item.find(".item_a_a").bind("click",function(){
            window.open(value[2]);
        })
        item.find(".item_c").text(value[3]);
        item.find(".item_d").find("span").text("百度快照");
        item.find(".item_d").bind("click",function(){
            window.open( value[4]);
        })

        content.append(item);
		
    })

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