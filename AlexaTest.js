//Testing algorithm for Alexa
//tester must give skill refresh tokens, and the names of audiofiles to be sent to alexa
//also give refresh token for user for voice command API

var globalRefreshTokens = [{token: "Atzr|IwEBIKg36_U1AAh1kMFMFUHiRDivvfgIBofs7GUMsVJ18axqqNUcrCI7EixmVPVtYVXLN3xx7nvbPUWamHJjr_9wv2-hIoZ1L4snXdY6HmQ0lRPzLPy0T5PN_-qsG9QNNHsHjopBoYZgRbmscJco7l_X-sZgHKqnhAcQhq_uA29XXdAZW8aC6FlEAgtJnjP3XiAmEcFQh10vvaai7z-8jqtBm4qH393USKTOHKfND2oy-ORlGSdAkVHQtCDMZa7cMn_i1p7HgfSKD0I72QAbx-jeSdr-", clientID: "amzn1.application-oa2-client.ae4579aa2a10481b814c3a81efeb12c8", clientSecret: "7e5fcc59a72f90995473275deea7dfd9dd13811d251c8b99f854942edc083e96"}] //array of objects, one for each skill containing refresh token, client ID of skill and client secret of skill
//Example: [{token: "Atzr|abcd", clientID: "amzn1.application-oa2-client.e582ec497d5745f6b7a7c427e813eb03", clientSecret: "08fd2a70e..." }]

const https = require('https')
// var query = require('cli-interact').getYesNo;
const fs = require('fs');
const http2 = require('http2');

const readline = require("readline").createInterface({
  input: process.stdin,
  output: process.stdout
});

var globalTokens = []
function refresh(refresh){
    var token;
    const data = "grant_type=refresh_token&refresh_token=" + refresh.token + "&client_id=" + refresh.clientID  + "&client_secret=" + refresh.clientSecret
    const options = {
      hostname: 'api.amazon.com',
      path: '/auth/o2/token',
      method: 'POST',
      headers: {
        'Host': 'api.amazon.com',
        'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
      }
    }
    const req = https.request(options, res => {
      console.log(`statusCode: ${res.statusCode}`)

      res.setEncoding('utf8');
      res.on('data', (chunk) => {
        console.log(`BODY refresh: ${chunk}`);
        token = JSON.parse(chunk).access_token;

        globalTokens[globalTokens.length] = token
      });
      res.on('end', () => {
        console.log('No more data in response.');
      });
    })
    req.write(data)
    req.end()

}

for(var i = 0; i < globalRefreshTokens.length; i++){
  refresh(globalRefreshTokens[i])
}

var voiceAuth;
function refresh_voice_auth(){
    var token;
    const data = "grant_type=refresh_token&refresh_token="
      + //authorization token for test user for SpeechRecognizer API
      + "&client_id=" + //test VA device id
      + "&client_secret=" + //test VA device secret
    const options = {
      hostname: 'api.amazon.com',
      path: '/auth/o2/token',
      method: 'POST',
      headers: {
        'Host': 'api.amazon.com',
        'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
      }
    }
    const req = https.request(options, res => {
      console.log(`statusCode: ${res.statusCode}`)

      res.setEncoding('utf8');
      res.on('data', (chunk) => {
        console.log(`BODY: ${chunk}`);
        token = JSON.parse(chunk).access_token;
        voiceAuth = token;
      });
      res.on('end', () => {
        console.log('No more data in response.');
      });
    })
    req.write(data)
    req.end()

}
refresh_voice_auth();







const vaRaw= fs.readFileSync('./va.json'); 
var vaData = JSON.parse(vaRaw);
var vaCount = Object. keys(vaData.VA). length;
console. log(vaCount);
console.log(vaData.VA.alexa1.location);

const deviceRaw= fs.readFileSync('./devices.json'); 
var deviceData = JSON.parse(deviceRaw);
console.log(deviceData);
var deviceCount = Object. keys(deviceData.SmartHomeDevice). length;
console. log(deviceCount);
console.log(deviceData.SmartHomeDevice.light2.Device_Location);

const vcRaw= fs.readFileSync('./vc.json'); 
var vcData = JSON.parse(vcRaw);
console.log(vcData);
var vcCount = Object. keys(vcData.VoiceCommand). length;
console.log(vcCount);

var raw_names = [];
var raw_types = [];
var raw_manufacturer = [];
Object.entries(deviceData.SmartHomeDevice).forEach((entry) => {
  const [key, value] = entry;
  console.log(`${key}: ${value}`);
  console.log(key);
  console.log(deviceData.SmartHomeDevice[key]);
  console.log("device loc:", deviceData.SmartHomeDevice[key].Device_Location);
  raw_names.push(deviceData.SmartHomeDevice[key].Device_Name);
  raw_types.push(deviceData.SmartHomeDevice[key].Device_Type);
  raw_manufacturer.push(deviceData.SmartHomeDevice[key].Device_Manufacturer);
});
console.log("device count: ", [deviceCount]);
console.log("names: ", [raw_names]);
console.log("types: ", [raw_types]);
console.log("types: ", [raw_manufacturer]);

//MAIN
main(globalTokens)


//issue voice command from inputs wav file
function command(filename){
  fs.readFile(filename, function(err, content){
      if(err){
          console.log(err);
      }
      var metadata = JSON.stringify(
  	{
  	    "context": [
  	        {
  	            "header": {
  	                "namespace": "SpeechRecognizer",
  	                "name": "RecognizerState"
  	            },
  	            "payload": {

  	            }
  	        },
  	        {
  	            "header": {
  	                "namespace": "Speaker",
  	                "name": "VolumeState"
  	            },
  	            "payload": {
  	                "volume": 10,
  	                "muted": false
  	            }
  	        },
  	        {
  	            "header": {
  	                "namespace": "Alerts",
  	                "name": "AlertsState"
  	            },
  	            "payload": {
  	                "allAlerts": [],
  	                "activeAlerts": []
  	            }
  	        },
  	        {
  	            "header": {
  	                "namespace": "SpeechSynthesizer",
  	                "name": "SpeechState"
  	            },
  	            "payload": {
  	                "token": "",
  	                "offsetInMilliseconds": 0,
  	                "playerActivity": "FINISHED"
  	            }
  	        },
  	        {
  	            "header": {
  	                "namespace": "AudioPlayer",
  	                "name": "PlaybackState"
  	            },
  	            "payload": {
  	                "token": "",
  	                "offsetInMilliseconds": 0,
  	                "playerActivity": "IDLE"
  	            }
  	        }
  	    ],
  	    "event": {
  	        "header": {
  	            "namespace": "SpeechRecognizer",
  	            "name": "Recognize",
  	            "messageId": "1eff3c5e-02e3-4dd3-9ca0-7c38937f005f",
  	            "dialogRequestId": "a905c2bb-1bbd-45cf-9f85-6563d2546492"
  	        },
  	        "payload": {
  	            "profile": "FAR_FIELD",
  	            "format": "AUDIO_L16_RATE_16000_CHANNELS_1"
  	        }
  	    }
  	});
  	var data = "--this-is-my-boundary-for-alexa\r\n";
  	data += 'Content-Disposition: form-data; name="metadata"\r\n';
  	data +='Content-Type: application/json; charset=UTF-8\r\n\r\n';
  	data += metadata;
  	data += "\r\n";
  	data += "--this-is-my-boundary-for-alexa\r\n";
      data += "Content-Disposition: form-data; name=\"audio\"\r\n";
      data += "Content-Type:application/octet-stream\r\n\r\n";
      var payload = Buffer.concat([
              Buffer.from(data, "utf8"),
              new Buffer(content, 'binary'),
              Buffer.from("\r\n--this-is-my-boundary-for-alexa\r\n", "utf8"),
      ]);

      const client = http2.connect('https://avs-alexa-na.amazon.com:443');

      client.on('error', (err) => console.log({payload:err}));
      client.on('socketError', (err) => console.log({payload:err}));

      var request = {
  	    ':method' : 'POST',
  	    ':scheme' : 'https',
  	    ':path' : '/v20160207/events',
  	    'authorization' : 'Bearer '+ voiceAuth,
  	    'content-type' : 'multipart/form-data; boundary=this-is-my-boundary-for-alexa'
      };

      var req = client.request(request);

  	req.on('response', (headers, flags) => {
  	    for (const name in headers) {
              if(name === ':status') {
                  console.log("command response")
                  console.log({payload:`${name}: ${headers[name]}`});
              }
          }
  	});

  	req.on('error', function(err) {
  	  console.log(err);
  	});

  	req.setEncoding('utf8');
  	let outdata = '';
  	req.on('data', (chunk) => { outdata += chunk; });
  	req.on('end', () => {

  	});

  	req.write(payload);
  	req.end();
  });
}

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

async function main(tokens) {
  await sleep (2000); //wait for async tokens to be resolved
  var numTokens = tokens.length;

  var endpointInc = 0;
  var totalDevices = [deviceCount];
  var names = [raw_names];
  var types = [raw_types];
  var manufacturers = raw_manufacturer;
  var voiceCommandFiles = [] //fill will files containing audio that will be send i.e. ["file1.wav"]
  var trialNum = 0
  //grid based loop on inputs, add devices then issue voice commands
  for(var k = 0; k < totalDevices.length; k++){
    for(var j = 0; j < names.length; j++){
      for(var t = 0; t < types.length; t++){
          endpointInc = 0;

          for(var i = 0; i < totalDevices[k]/25; i++){
            for(var m = 0; m < numTokens; m++){
                var endpoints = []
                if(totalDevices[k]-i*25 < 25){ //batches of 25 untill less than 25 left
                    endpoints = automated(totalDevices[k]-i*25, names[j], types[t], trialNum, endpointInc, manufacturers)
                    endpointInc += totalDevices[k]-i*25
                }else{
                    endpoints = automated(25, names[j], types[t], trialNum, endpointInc, manufacturers)
                    endpointInc += 25;
                }

                var msg = {
                  "event": {
                    "header": {
                      "namespace": "Alexa.Discovery",
                      "name": "AddOrUpdateReport",
                      "payloadVersion": "3",
                      "messageId": "504c9752-d722-4eb4-98dd-8fe9e82b89af"
                    },
                    "payload": {
                      "endpoints": endpoints,
                      "scope": {
                        "type": "BearerToken",
                        "token": tokens[m]
                      }
                    }
                  }
                }
                normalReq(msg, tokens[m])
                await sleep(500)
            }
          }

          await sleep (60*1*totalDevices[k] + 5000); //make sure devices are added before voice commadn
          for(var v = 0; v < voiceCommandFiles.length; v++){
            //command(voiceCommandFiles[v])
            var appDate = Date.now()/10
            appDate = Math.round(appDate%100000000) //lower bits of time
            fs.appendFileSync('logs.txt', trialNum + " " + appDate + " " + numTokens + '\n');
            await sleep (60*5*totalDevices[k] + 5000);
          }

          endpointInc = 0

          for(var i = 0; i < totalDevices[k]/25; i++){
            for(var m = 0; m < numTokens; m++){
              var endpoints = []
              if(totalDevices[k]-i*25 < 25){ //batches of 25 untill less than 25 left
                  endpoints = automated(totalDevices[k]-i*25, names[j], types[t], trialNum, endpointInc, manufacturers)
                  endpointInc += totalDevices[k]-i*25
              }else{
                  endpoints = automated(25, names[j], types[t], trialNum, endpointInc, manufacturers)
                  endpointInc += 25;
              }

            var msg = {
              "event": {
                "header": {
                  "namespace": "Alexa.Discovery",
                  "name": "DeleteReport",
                  "payloadVersion": "3",
                  "messageId": "504c9752-d722-4eb4-98dd-8fe9e82b89af"
                },
                "payload": {
                  "endpoints": endpoints,
                  "scope": {
                    "type": "BearerToken",
                    "token": tokens[m]
                  }
                }
              }
            }
            //normalReq(msg, tokens[m])
            await sleep(4000)
          }
        }
        trialNum++;
    }
   }
  }
}

//generates device information array from inputs
function automated(devices, names, types, trialNum, endpointInc, manufacturers){
  var currType = 0;
  var numTypes = types.length
  var numNames = names.length
  var numMans = manufacturers.length
  var currMan = 0;
  var namesInc = 0;
  var arr = []
  for(var i = 0; i < devices; i++){
    var el =   {
          "endpointId":  trialNum.toString() + "_" + endpointInc.toString(),
          "manufacturerName": manufacturers[currMan],
          "description": "Smart Light by Sample Manufacturer",
          "friendlyName": names[namesInc],
          "additionalAttributes":  {
            "manufacturer" : "Sample Manufacturer",
            "model" : "Sample Model",
            "serialNumber": trialNum,
          },
          "displayCategories": [types[currType]],
          "cookie": {},
          "capabilities": [
            {
              "type": "AlexaInterface",
              "interface": "Alexa.PowerController",
              "version": "3",
              "properties": {
                "supported": [
                  {
                    "name": "powerState"
                  }
                ],
                "proactivelyReported": true,
                "retrievable": false
              }
            },
          ],
          "connections": [
          ]
        }

      arr[i] = JSON.parse(JSON.stringify(el));

      endpointInc++;
      namesInc = (++namesInc)
      if(namesInc == numNames){ //if we go back to first name, now increment type etc.
        namesInc = 0
        currType = (++currType)
        if(currType == numTypes){ //if we go back to first name, now increment type etc.
          currType = 0
          currMan = (++currMan)
          if(currMan == numMans){ //if we go back to first name, now increment type etc.
            currMan = 0
          }
        }
      }
  }
  console.log(arr)
  return arr
}

function normalReq(msg, token){
  const data = JSON.stringify(msg)

  const options = {
    hostname: 'api.amazonalexa.com',
    path: '/v3/events',
    method: 'POST',
    headers: {
      'Host': 'api.amazonalexa.com',
      'Authorization': "Bearer " + token,
      'Content-Type': 'application/json',
    }
  }
  const req = https.request(options, res => {
    console.log(`statusCode: ${res.statusCode}`)
    res.setEncoding('utf8');
    res.on('data', (chunk) => {
      console.log(`BODY: ${chunk}`);
    });
    res.on('end', () => {
      console.log('No more data in response.');
    });

  })
  req.write(data)
  req.end()
  console.log("addo rupdateReport")
}