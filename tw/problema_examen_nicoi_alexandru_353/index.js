const {response} = require('express');
const express = require('express');
const {Client}= require("pg");
const session = require('express-session');
const nodemailer= require('nodemailer');
const ejs=require('ejs');
const formidable = require('formidable');

var app=express();
app.use(session({secret: 'cf',saveUninitialized: true,resave: true}));
var sesi;
var client=new Client({ user: 'postgres', password:'postgres', database:'postgres', host:'localhost', port:5432 });
client.connect();
app.set("view engine","ejs");
app.use("/resurse", express.static(__dirname + "/resurse"));

app.get("/reviste", function(req, res){
    client.query(`select * from public.reviste`, function(err, rez){
        v_reviste=[];
        for(let elem of rez.rows){
            //console.log(elem.note);
            v_reviste.push(elem);

        }
        //console.log(v_elevi);
        res.render("pagini/reviste", {reviste: v_reviste});
    })
    
});

app.post("/reviste", function(req,res){
    var form = new formidable.IncomingForm();
    form.parse(req, function(err, fields, files){
        client.query(`select * from public.reviste`, function(err, rez){
            v_reviste=[];
            for(let elem of rez.rows){
                var sum = 0;
                var avg = elem.nrpagini/elem.pret;
                elem.avg = avg;
                v_reviste.push(elem);
            }
            v_reviste.sort(function(a,b){
                if (fields.cumsortez.toString().startsWith("cresc")) {
                    return (a.avg - b.avg);
                } else {
                    return -1 * (a.avg-b.avg);
                }
            })
            //console.log(v_elevi);
            res.render("pagini/reviste", {reviste: v_reviste});
        })
    });
});

app.get("/",function(req,res){
    res.render("pagini/index");
})

async function trimiteMail(antTematica, v_titluri, email){
    var transp= nodemailer.createTransport({
        service: "gmail",
        secure: false,
        auth:{//date login
            user:"tehniciwebalextrucks@gmail.com",
            pass:"pass123!!"
        },
        tls:{
            rejectUnauthorized:false
        }
    });
    var lista = "";
    console.log(v_titluri);
    for(let i = 0 ; i < v_titluri.length ; i++){ 
        if(i+1 == v_titluri.length){
            lista += `<li><i style="color:blue;">` + v_titluri[i].titlu + "</i></li>"
        } else {
        lista += "<li>" + v_titluri[i].titlu + "</li>"
        }
    }
    var last = v_titluri.pop();

    //genereaza html
    console.log(email);
    await transp.sendMail({
        from:"tehniciwebalextrucks@gmail.com",
        to:email,
        subject:"Poftim mailul",
        //text:`Esti mailul cu numarul ${count} la ora ${datetime}`,
        html:`<h1>Salut!</h1><p>${antTematica}</p><br><ol>${lista}</ol>`

    })
    console.log("trimis mail");
}

app.post("/emailtrimis", function(req, res){
    console.log("a intrat postul sau sal");
    var form = new formidable.IncomingForm();
    form.parse(req, function(err, fields, files){
        var tematica = fields.tematica;
        var mail = fields.email;
        var antTematica = "";
        if (!req.session.initialised) {
            req.session.initialised = true;
            sesi = req.session;
            sesi.tematicaAnt=tematica;
        } else {
            antTematica = sesi.tematicaAnt;
            sesi.tematicaAnt = tematica;
        }
        console.log(tematica);
        client.query(`select titlu from public.reviste where tematici like '%${tematica}%'`, function(err, rez){
            v_titluri = [];
            for(let elem of rez.rows){
                v_titluri.push(elem);
            };
            trimiteMail(antTematica, v_titluri, mail);
        });
        
        res.render("pagini/index")
    })

})

console.log("server starting...");
app.listen(8080);