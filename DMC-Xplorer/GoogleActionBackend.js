/**
 * Copyright 2018 Google Inc. All Rights Reserved.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
 const mysql = require('mysql');
 //logging database
 const connection = mysql.createConnection({
    host: "",
    user: "",
    password: "",
    database: "testbase"
  });

connection.connect((err) => {
  if (err) throw err;
    console.log('Connected!');
});


'use strict';

const functions = require('firebase-functions');
const {smarthome} = require('actions-on-google');
const {google} = require('googleapis');
const util = require('util');
const admin = require('firebase-admin');
// Initialize Firebase
admin.initializeApp();
const firebaseRef = admin.database().ref('/');
// Initialize Homegraph
const auth = new google.auth.GoogleAuth({
  scopes: ['https://www.googleapis.com/auth/homegraph'],
});
const homegraph = google.homegraph({
  version: 'v1',
  auth: auth,
});
// Hardcoded user ID
const USER_ID = '123';

exports.login = functions.https.onRequest((request, response) => {
  if (request.method === 'GET') {
    functions.logger.log('Requesting login page');
    response.send(`
    <html>
      <meta name="viewport" content="width=device-width, initial-scale=1">
      <body>
        <form action="/login" method="post">
          <input type="hidden"
            name="responseurl" value="${request.query.responseurl}" />
          <button type="submit" style="font-size:14pt">
            Link this service to Google
          </button>
        </form>
      </body>
    </html>
  `);
  } else if (request.method === 'POST') {
    // Here, you should validate the user account.
    // In this sample, we do not do that.
    const responseurl = decodeURIComponent(request.body.responseurl);
    functions.logger.log(`Redirect to ${responseurl}`);
    return response.redirect(responseurl);
  } else {
    // Unsupported method
    response.send(405, 'Method Not Allowed');
  }
});

exports.fakeauth = functions.https.onRequest((request, response) => {
  const responseurl = util.format('%s?code=%s&state=%s',
      decodeURIComponent(request.query.redirect_uri), 'xxxxxx',
      request.query.state);
  functions.logger.log(`Set redirect as ${responseurl}`);
  return response.redirect(
      `/login?responseurl=${encodeURIComponent(responseurl)}`);
});

exports.faketoken = functions.https.onRequest((request, response) => {
  const grantType = request.query.grant_type ?
    request.query.grant_type : request.body.grant_type;
  const secondsInDay = 86400; // 60 * 60 * 24
  const HTTP_STATUS_OK = 200;
  functions.logger.log(`Grant type ${grantType}`);

  let obj;
  if (grantType === 'authorization_code') {
    obj = {
      token_type: 'bearer',
      access_token: '123access',
      refresh_token: '123refresh',
      expires_in: secondsInDay,
    };
  } else if (grantType === 'refresh_token') {
    obj = {
      token_type: 'bearer',
      access_token: '123access',
      expires_in: secondsInDay,
    };
  }
  response.status(HTTP_STATUS_OK)
      .json(obj);
});

const app = smarthome();

function getTrialNum() {
  return new Promise((resolve, reject) => {
    connection.query(
      `SELECT TrialNum FROM testbase.Devices`,
      (err, result) => {
        return err ? reject(err) : resolve(result[0].TrialNum);
      }
    );
  });
}

app.onSync(async (body) => {
  functions.logger.log("SYNC respond")
  var trialNum = await getTrialNum();
  functions.logger.log(trialNum)
  var numDevices = [1,1000, 2000]
  var names = [["Bedroom"]]
  var types = [["TV"]]
  var numNames = names.length
  var numTypes = names.length
  var nameInc=0, typeInc=0, numInc = 0

  nameInc = trialNum%numNames
  typeInc = (trialNum%(numNames*numTypes)) / numNames
  numInc = trialNum / (numNames * numTypes)
  functions.logger.log("" + " " + names[nameInc] + " " + types[typeInc] + " " + numDevices[numInc] + " " + trialNum);
  var devArr;

  var devArr = automated(numDevices[numInc], names[nameInc], types[typeInc], trialNum);



  functions.logger.log("SYNC respond devArr" + devArr)
  functions.logger.log(JSON.stringify(devArr));
  return {
    requestId: body.requestId,
    payload: {
      agentUserId: USER_ID,
      devices: devArr,
    },
  };
});


function automated(devices, names, types, trialNum){
  var id = 1;
  var currType = 0;
  var numTypes = types.length
  var numNames = names.length
  var namesInc = 0;
  var arr = []
  for(var i = 0; i < devices; i++){
    var el =  {

          id:  id*100+trialNum,
          type: 'action.devices.types.' + types[currType],
          traits: [
            'action.devices.traits.OnOff',
          ],
          name: {
            defaultNames: [names[namesInc]],
            name: names[namesInc],
            nicknames: [names[namesInc]],
          },
          deviceInfo: {
            manufacturer: 'Acme Co',
            model: 'acme-washer',
            hwVersion: '1.0',
            swVersion: '1.0.1',
          },
          willReportState: true,
          attributes: {
            pausable: true,
          },

    }

    arr[i] = JSON.parse(JSON.stringify(el));

    namesInc = (++namesInc)
    if(namesInc == numNames){ //if we go back to first name, now increment type etc.
      namesInc = 0
      currType = (++currType)
      if(currType == numTypes){ //if we go back to first name, now increment type etc.
        currType = 0
        }
      }
      id++
  }
  return arr
}


const queryFirebase = async (deviceId) => {
  //const snapshot = await firebaseRef.child(deviceId).once('value');
  //const snapshotVal = snapshot.val();
  return {
    on: true
  };
};
const queryDevice = async (deviceId) => {
  const data = await queryFirebase(deviceId);
  return {
    on: data.on
  };
};

app.onQuery(async (body) => {
  const {requestId} = body;
  const payload = {
    devices: {},
  };
  const queryPromises = [];
  const intent = body.inputs[0];
  for (const device of intent.payload.devices) {
    const deviceId = device.id;
    queryPromises.push(
        queryDevice(deviceId)
            .then((data) => {
              // Add response to device payload
              payload.devices[deviceId] = data;
            }) );
  }
  // Wait for all promises to resolve
  await Promise.all(queryPromises);
  return {
    requestId: requestId,
    payload: payload,
  };
});

const updateDevice = async (execution, deviceId) => {
  const {params, command} = execution;
  let state; let ref;
  switch (command) {
    case 'action.devices.commands.OnOff':
      state = {on: params.on};
      ref = firebaseRef.child(deviceId).child('OnOff');
      var trialNum = deviceId%100;
      break;
    case 'action.devices.commands.StartStop':
      state = {isRunning: params.start};
      ref = firebaseRef.child(deviceId).child('StartStop');
      break;
    case 'action.devices.commands.PauseUnpause':
      state = {isPaused: params.pause};
      ref = firebaseRef.child(deviceId).child('StartStop');
      break;
  }

  return ref.update(state)
      .then(() => state);
};

app.onExecute(async (body) => {
  const {requestId} = body;
  console.log("EXECUTE + TRIALNUM: " + trialNum)
  // Execution results are grouped by status
  const intent = body.inputs[0];
  var trialNum = intent.payload.commands[0].devices[0].id%100
  var length = intent.payload.commands[0].devices.length

  var sqlStr = `INSERT INTO testbase.Logs (TrialNum, Skill, Time, NumCommands)
    VALUES (`+ trialNum +`, `+1+`, `+ Math.round(Date.now()%100000000/10) +`, `+  + `);`;

  connection.query(sqlStr , (err, result, fields) => {
  });

  const result = {
    ids: [],
    status: 'SUCCESS',
    states: {
      online: true,
    },
  };


  var ensureId=1
  for (const command of intent.payload.commands) {
    for (const device of command.devices) {
      result.ids.push(device.id)
      if(ensureId!=device.id)
        functions.logger.log("device didnt get reqest")
      ensureId++
    }
  }
  return {
    requestId: requestId,
    payload: {
      commands: [result],
    },
  };
});

app.onDisconnect((body, headers) => {
  functions.logger.log('User account unlinked from Google Assistant');
  // Return empty response
  return {};
});

exports.smarthome = functions.https.onRequest(app);

exports.requestsync = functions.https.onRequest(async (request, response) => {
  response.set('Access-Control-Allow-Origin', '*');
  functions.logger.info(`Request SYNC for user ${USER_ID}`);
  try {
    const res = await homegraph.devices.requestSync({
      requestBody: {
        agentUserId: USER_ID,
      },
    });
    functions.logger.info('Request sync response:', res.status, res.data);
    response.json(res.data);
  } catch (err) {
    functions.logger.error(err);
    response.status(500).send(`Error requesting sync: ${err}`);
  }
});

exports.updatetrial = functions.https.onRequest((request, response) => {
  var sqlStr = "UPDATE testbase.Devices SET TrialNum = " + request.body.value
  functions.logger.log("SQL: " + sqlStr)
  connection.query(sqlStr , (err, result, fields) => {
    functions.logger.log("updated")
  });
  return {}
});



function sleep(duration) { return new Promise(resolve => setTimeout(duration, resolve)); }
/**
 * Send a REPORT STATE call to the homegraph when data for any device id
 * has been changed.
 */
exports.reportstate = functions.database.ref('{deviceId}').onWrite(
    async (change, context) => {
      functions.logger.info('Firebase write event triggered Report State');
      //const snapshot = change.after.val();

      const requestBody = {
        requestId: 'ff36a3cc', /* Any unique ID */
        agentUserId: USER_ID,
        payload: {
          devices: {
            states: {
              /* Report the current state of our washer */
              [context.params.deviceId]: {
                on: true
              },
            },
          },
        },
      };

      const res = await homegraph.devices.reportStateAndNotification({
        requestBody,
      });
      functions.logger.info('Report state response:', res.status, res.data);
    });
