    //load variantvalue options


    $(window).on("load", function(){
      get_variantvalues_source()
    
    });  
    
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
        console.log(variants)   
    }      
         

