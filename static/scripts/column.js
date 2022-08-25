const x = document.querySelector('input[type=file]');


x.addEventListener("change",(e)=>{
    const fr = new FileReader();
    fr.onloadend=e=>{
        let r = fr.result.split("\n");
        var headers = r[0].split(',');
        document.myform.myinput.value = r;
        console.log(headers)
        }

    fr.readAsText(x.files[0]);

});


