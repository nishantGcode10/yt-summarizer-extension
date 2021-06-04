var percent = 50;
document.getElementById('myslider').addEventListener('input', function (e) {

    console.log(typeof e.target.value);
    percent = parseInt(e.target.value);
    document.getElementById('per').innerHTML = e.target.value + "%";


});
var myurl = "";
document.getElementById('mybut').onclick = function (e) {
    e.preventDefault();
    console.log('im here');
    document.getElementById('summary').innerHTML="Please Wait...";
    var query = { active: true, currentWindow: true };
    try{
    chrome.tabs.query(query, function callback(tabs) {
        var currentTab = tabs[0]; // there will be only one in this array
        myurl = currentTab.url// also has properties like currentTab.id
        console.log(currentTab.url);
        console.log(myurl);
        var requestData ={
            'content':myurl,
            'percent':percent,
        };
       
        fetch('http://127.0.0.1:5000/link',{
                method:'POST',
                headers: {
                    'Content-Type': 'application/json'
                    // 'Content-Type': 'application/x-www-form-urlencoded',
                  },
                  body: JSON.stringify(requestData)
        }).then(res=>res.json()).then(data=> document.getElementById('summary').innerHTML=data);
    });
}
catch(e){
    document.getElementById('summary').innerHTML=e,message;
}
    console.log(myurl);
    

}
