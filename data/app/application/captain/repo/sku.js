    //load variantvalue options


    $(window).on("load", function(){
      get_variantvalues_source()
    
    });  
    
    function get_variantvalues_source() {
        var x = document.getElementById('variantvalues_source');
         var txt = "";
         var val = "";
         for (var i = 0; i < x.length; i++) {
             txt +=x[i].text + ",";
             val +=x[i].value + ",";
          }
        console.log(val)   
    }      
         

