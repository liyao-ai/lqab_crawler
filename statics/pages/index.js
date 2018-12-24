$(function(){
  // 初始化方法
  init();

  initselect();
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
    var url = "/search/"+plant+"/"+keyword;
    ajaxPost(url,null,successSearch,50000,errorSearch)
}
// 请求数据完成
function successSearch(result){
    var keyword = $("#keyword").val();
    if(result.length==0){
        var url = "/crawler/"+plant+"/"+keyword;
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
        item.find(".item_d").find("span").text(value.search_plant+"快照");
        item.find(".item_d").bind("click",function(){
            window.open( value.snapshot);
        })

        content.find("#show_table_id").find("#collapseTable").find(".row").append(item);
    })
    var random = parseInt(Math.random()*(200-100+1)+100);
    content.find("a").attr("href","#关键字"+keyword+random);
    content.find("#show_table_id").find("#collapseTable").attr("id","关键字"+keyword+random);

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

// -- 平台下拉选择    ---------------------------
var logoData=[{
    plant:"360",
    imgSrc: '/statics/img/360_logo.png'
},{
    plant:"百度",
    imgSrc:'/statics/img/baidu_logo.png'
},{
    plant:"搜狗",
    imgSrc:'/statics/img/sougou_logo.png'
}]
function toggleFlag () {
    $(".logoList").css({"display":""});
}

function initselect(){
    var ul = $(".logoList");
    $.each(logoData,function(index,value){
        if(index==1){
            plant = value.plant;
        }
        var li = $(' <li class="logoItem"><img /></li>');
        li.find("img").attr("src",value.imgSrc);
        li.bind("click",function(){
            logoSelected(index);
        })
        ul.append(li);
    })
     $(".logoList").css({"display":"none"});
}

function logoSelected (index) {
    $.each(logoData,function(ind,value){
        if(index == ind){
            $("#showLogohead").attr("src",value.imgSrc);
             plant = value.plant;
        }
    })
    $(".logoList").css({"display":"none"});
}