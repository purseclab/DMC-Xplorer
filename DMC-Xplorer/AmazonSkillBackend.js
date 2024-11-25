const AWS = require('aws-sdk')
const rdsData = new AWS.RDSDataService()

exports.handler = function (request, context) {
    const https = require('https')

    if (request.directive.header.namespace === 'Alexa.Discovery' && request.directive.header.name === 'Discover') {
        log("DEBUG:", "Discover request",  JSON.stringify(request));
        handleDiscovery(request, context, "");
    }
    else if (request.directive.header.namespace === 'Alexa.PowerController') {
        if (request.directive.header.name === 'TurnOn' || request.directive.header.name === 'TurnOff') {
            log("DEBUG:", "TurnOn or TurnOff Request", JSON.stringify(request));
            handlePowerControl(request, context);
        }
    }else if (request.directive.header.name === "AcceptGrant"){
        console.log("ACCEPTGRANT: " + JSON.stringify(request));
         const data = "grant_type=authorization_code&code="
          + request.directive.payload.grant.code
          + "&client_id=" +// skill client ID 
          + "&client_secret="//skill client secret
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
          });
          res.on('end', () => {
            console.log('No more data in response.');
          });
           context.succeed({
              "event": {
                "header": {
                  "namespace": "Alexa.Authorization",
                  "name": "AcceptGrant.Response",
                  "messageId": "<message id>",
                  "payloadVersion": "3"
                },
                "payload": {}
              }
            })
        })
        req.write(data)
        req.end()
    }else{
        console.log("Unhandled request: " + request.directive.header.name);
    }

    function handleDiscovery(request, context) {
        var responseHeader = request.directive.header;
        var messageID = responseHeader.messageId
        var endpointArray = []
      //   var endpointArray = [{ can add inital devices or not
      //       "endpointId": "1",
      //       "manufacturerName": "Sonos",
      //       "description": "Description",
      //       "friendlyName": "Skill-1 Light",
      //       "additionalAttributes":  {
      //       },
      //       "displayCategories": ["LIGHT"],
      //       "cookie": {},
      //       "capabilities": [
      //         {
      //           "type": "AlexaInterface",
      //           "interface": "Alexa.PowerController",
      //           "version": "3",
      //           "properties": {
      //             "supported": [
      //               {
      //                 "name": "powerState"
      //               }
      //             ],
      //             "proactivelyReported": true,
      //             "retrievable": true
      //           }
      //         },
      //       ],
      //       "connections": [
      //       ]
      // } ]

        var payload = {
            "endpoints": endpointArray

        };
        var header = request.directive.header;
        header.name = "Discover.Response";
        log("DEBUG", "Discovery Response: ", JSON.stringify({ header: header, payload: payload }));
        context.succeed({ event: { header: header, payload: payload } });
    }

    function log(message, message1, message2) {
        console.log(message + message1 + message2);
    }

    function handlePowerControl(request, context) {


      var TrialNum = request.directive.endpoint.endpointId.split("_")[0];
      var currTime = Date.now();
      currTime = Math.trunc(currTime/10) //drop miliseconds
      currTime = currTime%100000000  //drop most significant bits to just get hours-sec
      //AWS RDS with accessable API credentials
      //Skill num is set to 1 but changes for each skill
      let updateParams = {
        secretArn: //database secretArn for amazon RDS
        ,
        resourceArn: //database resourceArn for amazon RDS
        ,
       sql: 'INSERT INTO Trials (TrialNum, Time, SkillNum) VALUES ("'+TrialNum+'", "'+currTime+'", "'+1+'");',
       database: 'testbase',
       includeResultMetadata: true
      }
      rdsData.executeStatement(updateParams, function (err, newdata) {
        if(err){
          console.log(err)
        }else{
          wait(request, context)
        }
      })


    }
    function wait(request, context){
       // get device ID passed in during discovery
        var requestMethod = request.directive.header.name;
        var responseHeader = request.directive.header;
        responseHeader.namespace = "Alexa";
        responseHeader.name = "Response";
        responseHeader.messageId = responseHeader.messageId + "-R";
        // get user token pass in request
        var requestToken = request.directive.endpoint.scope.token;
        var powerResult;

        if (requestMethod === "TurnOn") {
          //always give SUCCESS
            powerResult = "ON";
        }
       else if (requestMethod === "TurnOff") {
          //always give SUCCESS
            powerResult = "OFF";
        }
        var contextResult = {
            "properties": [{
                "namespace": "Alexa.PowerController",
                "name": "powerState",
                "value": powerResult,
                "timeOfSample": "2017-09-03T16:20:50.52Z", //retrieve from result.
                "uncertaintyInMilliseconds": 50
            }]
        };
        var response = {
            context: contextResult,
            event: {
                header: responseHeader,
                endpoint: {
                    scope: {
                        type: "BearerToken",
                        token: requestToken
                    },
                    endpointId: request.directive.endpoint.endpointId
                },
                payload: {}
            }
        };
        log("DEBUG", "Alexa.PowerController ", JSON.stringify(response));
        context.succeed(response);
    }
};
