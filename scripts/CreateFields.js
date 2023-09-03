var jsforce = require('jsforce');

// run this script with command `node scripts/CreateFields.js`

// Your obtained Session ID and instance URL
const sessionId = ''; // Get this by viewing source on the developer console and searching for sid
const instanceUrl = ''; // e.g., 'https://xxx.my.salesforce.com'

const conn = new jsforce.Connection({
  instanceUrl: instanceUrl,
  accessToken: sessionId
});

// Fetch identity information of the authenticated user
conn.identity((err, identity) => {
  if (err) {
    console.error("Error fetching identity:", err);
    return;
  }

  console.log("User ID:", identity.user_id);
  console.log("Username:", identity.username);
  console.log("Display Name:", identity.display_name);
  console.log("Organization ID:", identity.organization_id);
  // ... you can log other properties as needed
});

// create a function to accept object, fieldname, and fieldtype that uses the jsforce metadata api to create a new field on the object
function createField(object, fieldname, fieldtype) {


    // based on samplemetadata create a real metadata variable populated by the input.  There should not be a lenght property at all for date.
    var metadata = [{
        fullName: object + '.' + fieldname,
        label: fieldname,
        length: 50,
        type: fieldtype
    }];

    // delete the lenght property if it is a date field
    if (fieldtype == 'Date') {
        delete metadata[0].length;
    }


    conn.metadata.create('CustomField', metadata, function(err, results) {
        if (err) { console.error(err); }
        console.log(results);
    });

}

// use the createfield to create a new field on Player__c called Player_Location__c
createField('Player__c', 'Player_Location__c', 'Text');
// dataofbirth
createField('Player__c', 'DateOfBirth__c', 'Date');

