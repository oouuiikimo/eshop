    //load variantvalue options

    $(window).on("load", function(){
      get_variantvalues_source()
      //console.log(detail_id)
    });  

    function selectButtons(name,arr,sel) {
                     
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
    
    function get_variantvalues_source() {
        var x = document.getElementById('variantvalues_source');

         let variants = {}
         for (var i = 0; i < x.length; i++) {
             let variant = x[i].text.split('_')
             //console.log(variant[0])
             if (!variants.hasOwnProperty(variant[0])) {
                variants[variant[0]]=[{"id":x[i].value,"value":variant[1]}]
             }
             else 
                variants[variant[0]].push({"id":x[i].value,"value":variant[1]}) 
             
          }
        Object.keys(variants).forEach(key => selectButtons(key,variants[key],0))  
        //console.log(variants)   
    }      
         

