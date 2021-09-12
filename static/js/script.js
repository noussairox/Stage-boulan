document.querySelector('.img_btn').setAttribute("onclick", "location.href='/'")
var a;
function show_hide(){
    if(a==1){
        document.querySelector('#myform').style.display="inline";
        return a=0;
    }
    else
        document.querySelector('#myform').style.display="none"
        return a=1;
}