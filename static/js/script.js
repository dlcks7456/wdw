function Request(){
    var requestParam ="";

	//getParameter Æa¼C
	this.getParameter = function(param){
        var url = unescape(location.href);
        var paramArr = (url.substring(url.indexOf("?")+1,url.length)).split("&");

        for(var i = 0 ; i < paramArr.length ; i++){
           var temp = paramArr[i].split("="); //ÆA¶o¹IAI º?¼o¸iA≫ ´aA½

           if(temp[0].toUpperCase() == param.toUpperCase()){
             requestParam = paramArr[i].split("=")[1];
             break;
           }
        }
        return requestParam;
    }
}

function getpid(){
	var url = unescape(location.href);
	var pid = url.split("/").reverse();
	return pid[1];
}


function LoginOK(f){
	if(f.UID.value==""){
	  //ID Check error msg
		alert("ID를 입력해주세요");
		f.UID.focus;
	}else{ //추가적인 validate는 else if 로 추가
 		var request = new Request();
    //list = 1 디폴트
		f.list.value = request.getParameter("list")=='' ? 1 : request.getParameter("list") ;


    //리다이렉트할 링크 (별도 수정 안해도됨)
		f.action = "https://pacific.surveys.nielseniq.com/survey/selfserve/548/"+getpid();
		f.submit();
	}
}

function rangechk(value,errclass){
  if( !(value>=0 && value<=99) ){
    $(errclass).show();
  }else{
    $(errclass).hide();
  }
}

function delete_check(url){
    if( confirm("해당 데이터를 삭제합니다.") ){
        alert("삭제 되었습니다.");
        $(location).attr('href',url);
    }else{
        return false;
    }
}

// datacheck page script
$(document).ready(function(){
    $("input[name=checkdata_all]").click(function(){
        if( $("input[name=checkdata_all]").is(":checked") ){
            $("input[name=checkdata]").prop("checked",true);
        }else{
            $("input[name=checkdata]").prop("checked",false);
        }
    });

    $("input[name=checkdata]").click(function(){
        var rows = $("input[name=checkdata]").length;
        var check_rows = $("input[name=checkdata]:checked").length;
        if( rows==check_rows ){
            $("input[name=checkdata_all]").prop("checked",true);
        }else{
            $("input[name=checkdata_all]").prop("checked",false);
        }
    });

    $("input[name=deleterow]").click(function(){
        var check_rows = $("input[name=checkdata]:checked").length;
        if( check_rows==0 ){
            alert("선택된 데이터가 없습니다.");
            return false;
        }else{
            if( confirm("선택한 데이터를 삭제합니다.") ){
                alert("삭제 되었습니다.");
                return true;
            }else{
                return false;
            }
        }
    });

});

function comparespider(){
    var checks = [];
    $("input:checkbox[name=checkdata]:checked").each(function(){
        checks.push($(this).val());
    });

    if( checks.length == 0 ){
        alert("비교 대상을 선택해주세요.");
        return false;
    }
    else if( checks.length == 1 ){
        alert("2명 이상 선택해주세요.");
        return false;
    }
    else if( checks.length >= 6 ){
        alert("5명 이하로 선택해주세요.");
        return false;
    }else{
        return true;
    }
}


//SLIDESHOW
var slideIndex = 1;
showSlides(slideIndex);

// Next/previous controls
function plusSlides(n) {
  showSlides(slideIndex += n);
}

// Thumbnail image controls
function currentSlide(n) {
  showSlides(slideIndex = n);
}

function showSlides(n) {
  var i;
  var slides = document.getElementsByClassName("mySlides");
  var dots = document.getElementsByClassName("dot");
  if (n > slides.length) {slideIndex = 1}
  if (n < 1) {slideIndex = slides.length}
  for (i = 0; i < slides.length; i++) {
      slides[i].style.display = "none";
  }
  for (i = 0; i < dots.length; i++) {
      dots[i].className = dots[i].className.replace(" active", "");
  }
  slides[slideIndex-1].style.display = "block";
  dots[slideIndex-1].className += " active";
}


