

// Ajax请求对象
function createRequestObjects(){
    var ajaxRequest;
    try{
        // 非IE
        ajaxRequest = new XMLHttpRequest();
    }
    catch (e){
        // IE
        try{
            ajaxRequest = new ActiveXObject("Maxml2.XMLHTTP");
        }
        catch (e){
            try{
                ajaxRequest = new ActiveXObject("Microsoft.XMLHTTP");
            }
            catch (e){
                return false;
            }
        }
    }
    return ajaxRequest;
}


// 检查是否已经有OAuth授权的cookies
function checkOauthCookies(){
    var ajaxRequest = createRequestObjects();
    if(ajaxRequest != false){
        ajaxRequest.onreadystatechange = function(){
            if(ajaxRequest.readyState == 4){
                if(ajaxRequest.status == 200){
                    document.getElementById("");
                }
            }
        }// end callback function
        
        ajaxRequest.open("GET", "");
        ajaxRequest.send(null);
    }
    else{
        alert("Your browser is not support Ajax!")
    }
}


// 检查给定的参数是否有效
function checkIsValid(form, name){
    var value;
    if(name == "blog_name"){
        //value = document.getElementsByName("blog_name")[0].value;
        value = form.blog_name.value;
    }
    else if(name == "url_name"){
        //value = document.getElementsByName("url_name")[0].value;
        value = form.url_name.value;
    }

    var ajaxRequest = createRequestObjects();
    if(ajaxRequest != false){
        ajaxRequest.onreadystatechange = function(){
            if(ajaxRequest.readyState == 4){
                if(ajaxRequest.status == 200){
                    document.getElementById("check_" + name).innerHTML=ajaxRequest.responseText;
                }
            }
        }// end callback function
        ajaxRequest.open("GET", "/dropbox/check/" + name + "/" + value);
        ajaxRequest.send(null);
    }
    else{
        alert("Your browser is not support Ajax!")
    }
}

// 保存blog_name和url_name
function saveSettings(form){
    if(document.getElementById("check_blog_name") != form.blog_name.value + "可用" ||
            document.getElementById("check_url_name") != form.url_name.value + "可用"){
        document.getElementById("setting_tips").innerHTML = '<strong style="color:red; font-size:10px;">请填写有效的Blog name和Url name!</strong>';
    }

    var ajaxRequest = createRequestObjects();
    if(ajaxRequest != false){
        ajaxRequest.onreadystatechange = function(){
            if(ajaxRequest.readyState == 4){
                if(ajaxRequest.status == 200){
                    document.getElementById("setting_tips").innerHTML='<strong style="color:#fff; font-size:10px;">保存成功</strong>'
                }
            }
        }// end callback function
        ajaxRequest.open("POST", "/dropbox/settings/");
        ajaxRequest.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
        ajaxRequest.send("blog_name="+form.blog_name.value+"&url_name="+form.url_name.value);
    }
    else{
        alert("Your browser is not support Ajax!")
    }
}
