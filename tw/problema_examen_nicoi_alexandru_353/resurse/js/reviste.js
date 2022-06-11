window.onload= function(){
    console.log(localStorage.getItem("pretMaximLS"));
    if (localStorage.getItem("pretMaximLS") === null) {
        localStorage.setItem("pretMaximLS", "0");
    }
    pretmaxim = localStorage.getItem("pretMaximLS");
    console.log(pretmaxim);
    var articole=document.getElementsByClassName("revista");
    for(let art of articole) {
        if(parseInt(art.getElementsByClassName("val-pret")[0].innerHTML, 10) < parseInt(pretmaxim, 10)) {
            art.style.border = "thick solid green"
        }
    }
    var btn=document.getElementById("filtrare");
    btn.onclick=function(){
        clickButtonFunction('filtering')
        articole=document.getElementsByClassName("revista");
        for(let art of articole){
            art.style.display="none";
            /*
            v=art.getElementsByClassName("nume")
            nume=v[0]*/
            var nume=art.getElementsByClassName("val-tematica")[0];//<span class="val-nume">aa</span>
            console.log(nume.innerHTML);
            var conditie1=nume.innerHTML.includes(getSelectedItem());
            if(conditie1) {
                art.style.display="grid";
            }
        }
    }
    var btnReset=document.getElementById("reset");
    btnReset.onclick=function(){
        var articole=document.getElementsByClassName("revista");
        for(let art of articole){
            art.style.display="grid";
        }
    }
    var rng=document.getElementById("inp-pret");
    rng.onchange=function(){
        var info = document.getElementById("infoRange");//returneaza null daca nu gaseste elementul
        if(!info){
            info=document.createElement("span");
            info.id="infoRange"
            this.parentNode.appendChild(info);
        }
        
        info.innerHTML="("+this.value+")";
    }
    var btnSetLocal=document.getElementById("setlocalstorage");
    btnSetLocal.onclick=function(){
        var info = document.getElementById("inp-pret").value;
        console.log(info);
        localStorage.setItem("pretMaximLS", info);
    }
}

function clickButtonFunction(counting) {
    console.log(counting);
    if (localStorage.getItem(counting) === null) {
        localStorage.setItem(counting, "0");
    }
    var value = parseInt(localStorage.getItem(counting));
    var newValue = value + 1
    localStorage.setItem(counting, newValue);
    document.getElementById(counting).innerHTML = newValue
}

function clickReset(counting) {
    localStorage.setItem(counting, "0");
    document.getElementById(counting).innerHTML = '0'
}


function getSelectItemThat(id) {
    for (var i = 1;i <= 4; i++)
    {
        document.getElementById(i).checked = false;
    }
    document.getElementById(id).checked = true;
}

function getSelectedItem() {
    for (var i = 1 ; i <= 4 ; i++) {
        if(document.getElementById(i).checked) {
            return document.getElementById(i).value;
        }
    }
}