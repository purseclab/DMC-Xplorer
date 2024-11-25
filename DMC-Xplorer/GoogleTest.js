//Runs the VadMax testing algorithm for google home assuming skills are already set up
//And each skill has an available requestsync URL which causes it to send a request sync
//Skill back-ends must read a trialNum from a database to determine which devices to add
//when they recieve a SYNC message


const mysql = require('mysql');
//Credentials for publically accessable amazon RDS databse
name = //name of SQL database scema
table = //name of table containing TrialNum column
const connection = mysql.createConnection({
   host: //database id e.g. database-2.cxggu7i7exq0.us-east-1.rds.amazonaws.com
   ,
   user: //user credentials
   ,
   password:
   ,
   database: name
 });

const http = require("http");
const https = require('https');
var query = require('cli-interact').getYesNo;

main()


async function other(){
  var sqlStr = "UPDATE " + name + "." + table + " SET TrialNum = 0"
    console.log("SQL: " + sqlStr)
    connection.query(sqlStr , (err, result, fields) => {
      console.log("updated")
  });
}

async function main(){ //just calls request sync and updates databsae since for google most work is done in skill back-end
  var runs = //number of runs i.e. num of devices * num names * num types * num manufacturers
  var urls = // array of request sync function URLs i.e. ["https://skill-3.web.app/requestsync"]
  for(var i = 0; i < runs; i++){

    var sqlStr = "UPDATE "+ name +"." + table + " SET TrialNum = " + i //database that firebase backend reads from
      console.log("SQL: " + sqlStr)
      connection.query(sqlStr , (err, result, fields) => {
        console.log("updated")
    });
    await sleep(3000);

    for(var i = 0; i < urls.length; i++){
      await https.get(urls[i], (res) => {
                  res.on('data', (d) => {
                  });
                  res.on('end', async (d) => {
                    console.log("reqsync")
                  });
              });
    }

    //change wait time based on method of issuing voice commands
    await sleep(20000);
    //give command
    await sleep(20000+60*numDevices[i]);
    console.log("adding the next set of devices")

  }

}


function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}
