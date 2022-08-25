const x = document.querySelector('input[type=file]');


x.addEventListener("change",(e)=>{
    const fr = new FileReader();
    fr.onloadend=e=>{
        let r = fr.result.split("\n")
        var jsonObj = [];
        var headers = r[0].split(',')
        console.log(headers)
        for(var i = 1; i < r.length; i++) {
                   var data = r[i].split(',');
                   var obj = {};
                   for(var j = 0; j < data.length; j++) {
                             obj[headers[j]] = data[j];

                    }

                   jsonObj.push(obj);
        }

        JSON.stringify(jsonObj);
        console.log(jsonObj)
        document.myform.myinput.value = jsonObj;
        var column = document.querySelector("input[class=column]");

        document.querySelector('form[class=pure-form]').addEventListener('submit', function (e) {
                 e.preventDefault();

                 console.log(column.value);

                 let sentences = []
                for(let i=0; i <jsonObj.length;i++){
                      let content = jsonObj[i][`${column.value}`]
                       sentences.push(content)
                       }
                if (headers.includes(column.value)){
                         document.myform.myinput.value = sentences;
                         console.log(sentences)
                 }


        });


    }
    fr.readAsText(x.files[0]);

})


