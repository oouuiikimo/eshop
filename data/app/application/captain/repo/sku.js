    //load variantvalue options

    $(window).on("load", function(){
        var values = document.getElementById('values')
        if (values && !detail_id) 
           //新增時
           get_variantvalues_source(true)
        if (detail_id && values)
            //編輯時
            //alert(detail_id + ':' + values.value)
            get_variantvalues_source(false)
            //show_values(values.value)
    });  

    function gen_input(name,ele) {
        let parent_div = document.createElement("div");
        parent_div.setAttribute("class", "form-group row"); 
        let _lable = document.createElement("label");
        _lable.setAttribute("class", "col-md-3 label-control"); 
        _lable.setAttribute("for", name); 
        _lable.innerHTML=name
        let _input_div = document.createElement("div");
        _input_div.setAttribute("class", "col-md-9"); 
        _input_div.appendChild(ele) 
        parent_div.appendChild(_lable)
        parent_div.appendChild(_input_div)
        return parent_div
    }
    
    function show_values(values) {
        let values_input = document.createElement("input");
        values_input.type="text"
        console.log(values)
        values_input.value= values//"Amsterdam,Washington,Sydney,Beijing,Cairo"
        values_input.setAttribute("data-role","tagsinput")
        values_input.setAttribute("disabled",true)
        
        
        document.getElementById("jsfields").appendChild(gen_input("屬性值",values_input))
    }
    function selectButtons(name,arr,sel,apply) {
                     
        let parent_div = document.createElement("div");
        parent_div.setAttribute("class", "form-group row"); 
        let _lable = document.createElement("label");
        _lable.setAttribute("class", "col-md-3 label-control"); 
        _lable.setAttribute("for", name); 
        _lable.innerHTML=name
        let _input_div = document.createElement("div");
        _input_div.setAttribute("class", "col-md-9"); 
        
        /*template: 
        <div class="form-group row">
        <label class="col-md-3 label-control" for="quantity">${name}</label>
        <div class="col-md-9"> 
        </div>
        </div>*/            
        
        var selectList = document.createElement("select");
        selectList.id = name;
        selectList.name = name;
        selectList.setAttribute("class", "form-control"); 
        selectList.setAttribute("onchange", "update_values();"); 
        if (!apply)
            selectList.setAttribute("disabled",true)
        //Create and append the options
        var option = document.createElement("option");
        option.value = '';
        option.text = '-請選擇-';
        selectList.appendChild(option);
        for (var i = 0; i < arr.length; i++) {
            var option = document.createElement("option");
            option.value = arr[i]["id"];
            option.text = arr[i]["value"];
            selectList.appendChild(option);  
            //console.log(arr[0])
        }
        selectList.selectedIndex = sel
        _input_div.appendChild(selectList)  
        
        parent_div.appendChild(_lable)
        parent_div.appendChild(_input_div)
        document.getElementById("jsfields").appendChild(parent_div)
        
    }
    
    function update_values() {
        let all_vals = []
        let all_sels = document.getElementById("jsfields").querySelectorAll('select')
        all_sels.forEach(item => all_vals.push(item.options[item.selectedIndex].value))
        document.getElementById("values").value = all_vals
    }
    
    function get_variantvalues_source(apply) {
        let sel = 0
        if (!apply) 
            sel = 1
        var x = document.getElementById('variantvalues_source');

         let variants = {}
         for (var i = 0; i < x.length; i++) {
             if (x[i].value == '0')
                 continue;
             let variant = x[i].text.split('_')
             //console.log(variant[0])
             if (!variants.hasOwnProperty(variant[0])) {
                variants[variant[0]]=[{"id":x[i].value,"value":variant[1]}]
             }
             else 
                variants[variant[0]].push({"id":x[i].value,"value":variant[1]}) 
             
          }
        Object.keys(variants).forEach(key => selectButtons(key,variants[key],sel,apply))  
        //console.log(variants)   
    }      
         

