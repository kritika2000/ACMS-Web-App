var express = require('express')
var app = express()
var dataForge = require('data-forge-fs')
var bodyParser = require('body-parser');
var createHTML = require('create-html')
const fs = require('fs') 


app.use(bodyParser.urlencoded({ extended: true }))
app.get('/', (req, res) => {
    res.sendFile(__dirname + '/home.html')
})
app.post('/tweets', (req, res) => {

    var sdate = req.body.startDate
    var edate = req.body.endDate

    if(sdate == "" || edate == ""){
        res.redirect(
            'http://localhost:5000/'
        )
    }
    else{
    var spawn = require('child_process').spawn; 

    var process = spawn('python', [__dirname + '/getCategories.py', 
                            sdate, 
                            edate]); 
    process.stdout.setEncoding('utf-8');

    process.stderr.on('data', function (data){
        console.log(data.toString())
    });
    process.stdout.on('data', function(data){
        response = data.toString()
        respJson = JSON.parse(response)
        console.log(respJson)
        var html = `<!DOCTYPE html>
        <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Tweets</title>
                <style>
                    p{
                        font-size: large;
                        font-weight: bold;
                        margin-left: 20px;
                    }
                    ul{
                        font-size: 19px;
                        font-weight:600;
                        text-decoration: underline;
                    }
                    ul li:hover{
                        color: #ff9900;
                        font-weight: bold;
                        text-decoration: underline;
                    }
                    table{
                        font-family: arial, sans-serif;
                        border-collapse: collapse;
                        width: 50%;
                        margin-left:20px
                      }
                      
                      td, th {
                        border: 1px solid #dddddd;
                        text-align: left;
                        padding: 8px;
                      }
                      
                      tr:nth-child(even) {
                        background-color: #dddddd;
                      }
                </style>
            </head>
            <body id = "body">
                <p>TOTAL NUMBER OF TWEETS - ${respJson["Total tweets"]}</p>
                <ul id = "list">
                    <li id = "positive", onclick = "posCategories()", style="font-weight: 500;">
                        Positive - ${respJson["Positive tweets"]}
                    </li>
                    <li id = "negative", onclick = "negCategories()", style="font-weight: 500;">
                        Negative - ${respJson["Negative tweets"]}
                    </li>
                    <li id = "neutral", style="font-weight: 500;">
                        Nuetral - ${respJson["Neutral tweets"]}
                    </li>
                </ul>
                <p id = 'demo'></p>
                <table id="tableneg" style="display:none;">
                    <tr>
                        <th>Categories</th>
                        <th>Count</th>
                    </tr>
                    <tr>
                        <td>Working</td>
                        <td>${respJson["working"]}</td>
                    </tr>
                    <tr>
                        <td>Secure</td>
                        <td>${respJson["secure"]}</td>
                    </tr>
                    <tr>
                        <td>Charge</td>
                        <td>${respJson["charge"]}</td>
                    </tr>
                    <tr>
                        <td>Time</td>
                        <td>${respJson["time"]}</td>
                    </tr>
                    <tr>
                        <td>Shipping</td>
                        <td>${respJson["shipping"]}</td>
                    </tr>
                    <tr>
                        <td>Delivery</td>
                        <td>${respJson["delivery"]}</td>
                    </tr>
                    <tr>
                        <td>Space</td>
                        <td>${respJson["space"]}</td>
                    </tr>
                    <tr>
                        <td>Location</td>
                        <td>${respJson["location"]}</td>
                    </tr>
                    <tr>
                        <td>Address</td>
                        <td>${respJson["address"]}</td>
                    </tr>
                </table>
                <table id="tablepos" style="display:none;">
                    <tr>
                        <th>Categories</th>
                        <th>Count</th>
                    </tr>
                    <tr>
                        <td>Timing of Delivery</td>
                        <td>${respJson["Timing of delivery"]}
                        </td>
                    </tr>
                    <tr>
                        <td>Space of Lockers</td>
                        <td>${respJson["Space of lockers"]}</td>
                    </tr>
                    <tr>
                        <td>Functionality of Lockers</td>
                        <td>${respJson["Functionality of lockers"]}</td>
                    </tr>
                    <tr>
                        <td>Location of lockers</td>
                        <td>${respJson["Location of lockers"]}</td>
                    </tr>
                    <tr>
                        <td>Charge of Lockers</td>
                        <td>${respJson["Charges of locker"]}</td>
                    </tr>
                    <tr>
                        <td>Security of Lockers</td>
                        <td>${respJson["Security of lockers"]}</td>
                    </tr>
                </table>
                <script>
                    var node_neg = document.getElementById('tableneg')
                    var node_pos = document.getElementById('tablepos')
                    function negCategories(){
                        document.getElementById("demo").innerHTML = "Negative Categories:"
                        node_neg.style.display = 'table';
                        node_pos.style.display = 'none';
                    }
                    function posCategories(){
                        document.getElementById("demo").innerHTML = "Positive Categories:"
                        node_neg.style.display = 'none';
                        node_pos.style.display = 'table';
                    }
                </script>
            </body>
        </html>`
        res.send(html)
    })
}   
})
app.listen(5000)
