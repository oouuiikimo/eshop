
var file_name = document.getElementById('file_name').value
var file = document.getElementById('file')
var imgid = "preview_pic"
$(window).on("load", function(){

    if (!detail_id) 
       //新增時
       show_pic()
    if (detail_id && file_name)
        //編輯時
        //alert(detail_id + ':' + values.value)
        alert('編輯')
        //show_values(file_name.value)
        
    file.addEventListener('change', (event) => {
    const _file = event.target.files[0];
    check_file_type(_file,imgid,resize_image_preview)
    //resize_image_preview(file)
  });    
});  

function show_pic(src="/shop/assets/images/none_1.jpg") {
    
    let img = document.createElement("img");
    img.src = src
    img.width = 200
    img.id = imgid
    img.onclick = function() {file.click();}
    img.setAttribute("style","cursor: pointer;");
    parentDiv = file.closest("div")
    parentDiv.appendChild(img)
}


