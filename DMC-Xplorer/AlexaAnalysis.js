//This analyzes the Alexa skill logs to find request delay for each trial logged in the database
//Assumptions made:
//Data stored in RDS database accessable through API calls
//Table contains the following data for each logged request by skill backend:
//    (TrialNum, Time, SkillNum)
//assumes logs.txt file contains the following data about each voice command given during testing:
//trialNum currentTime numSkills\n

const AWS = require('aws-sdk')
AWS.config.update({region:'us-east-1'});
const rdsData = new AWS.RDSDataService()

AWS.config.getCredentials(function(err) {
  if (err) console.log(err.stack);
  // credentials not loaded
  else {
    console.log("Access key:", AWS.config.credentials.accessKeyId);
  }
});

const fs = require('fs');

var minMax = []
var maxInc = 0;
var map = []

main();

async function main(){
  try {
  var data = fs.readFileSync('logs.txt', 'utf8')
  console.log(data)
  } catch (err) {
    console.error(err)
  }
  var tempArr = data.split("\n");
  var times = []
  for(var i = 0; i < tempArr.length; i++){
    var splitStr = tempArr[i].split(" ")
    map[splitStr[0]] = i
    times[i] = {}
    times[i].trial = splitStr[0]
    times[i].time = splitStr[1]
    times[i].numSkills = splitStr[2]
  }

  for(var k = 0; k < times.length; k++){
    console.log(times[k].trial)
    console.log(times[k].time)
    console.log(times[k].numSkills)
  }
  console.log("length")
  console.log(times.length)

  for(var i = 0; i < times.length - 1; i++){
    var res = []
    for(var k = 1; k < 2; k++){
      let sqlParams = {
          secretArn: //database secretArn for amazon RDS
          ,
          resourceArn: //database resourceArn for amazon RDS
          ,

          sql: `SELECT * FROM Trials WHERE
                ( (StartTime =
                    (SELECT Min(Time) FROM Trials WHERE
                        TrialNum = `+ times[i].trial +` AND SkillNum = `+ k +`))
                or
                (StartTime =
                    ((SELECT Max(Time) FROM Trials WHERE
                        TrialNum = `+ times[i].trial +` and SkillNum = `+ k +` ))))`

          ,



          database: 'testbase',
          includeResultMetadata: true
       }

       var test = 100
       await rdsData.executeStatement(sqlParams, function (err, data) {

        if (err) {
          // error
          console.log(err)

       } else {
         var min = 999999999999 //max starts large find minimum fastest time to first request
         var max = 0
         var locali = data.records[0][0].longValue

         for(var j = 0; j < data.records.length; j++){
           if(data.records[j][2].longValue > max){
             max = data.records[j][2].longValue
           }
           if(data.records[j][2].longValue < min){
             min = data.records[j][2].longValue
           }
         }
        minMax[maxInc] = {}
        minMax[maxInc].min = min
        minMax[maxInc].max = max
        console.log( String(locali) + " " + Math.round(min - times[map[locali]].time ) + " " + Math.round(max - times[map[locali]].time ));

      }
      })
    }

  }

}
