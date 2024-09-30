


<!-- Name of the example script -->
# Guide for using CURL for REST over Ethernet

<!-- Description of what the example script does -->
## Description

Curl can be used to send REST over Ethernet (RoE) requests to the TS4500 or Diamondback Tape Library. 
Once a user/script successfully logs into the library, the active session may be used to send further RoE requests to the library.
To close the session a logout request can be sent to the library.
Sessions left open will be closed, automatically, by the library once the session becomes inactive.

<!-- Description of how to use the script -->
## Usage
```
curl GET|-X POST https://<ip>/web/api/<endpoint> [-k][-v][-c filename][-b filename][-H header][-d data]
```
Arguments:

  * **GET**                             GET request type 
  * **-X POST**                         POST request type
  * **-X PUT**                          PUT request type
  * **<ip>**                            IP address or hostname of library 
  * **<endpoint>**                      REST API endpoint
  * **-k**                              Skip certificate validation. This is used for libraries with self-signed certificates.
  * **-v** 	                            Verbose
  * **-c**  	                        Store session ID in filename (used only for Login request)
  * **-b** 	                            Use session ID in filename. 
  * **-H** 	                            Adds header string to request header (used in POST|PUT)
  * **-d**	                            Sends data in POST, PATCH, DELETE request
  
<!-- Show product support information here -->
## Product Support

The curl examples were designed for the TS4500 and Diamondback tape libraries, and tested on code levels starting with 1.10.x.x and 2.10.x.x respectively.

<!-- Change history includes data and one line saying what changed -->
## Change History

  * July 19, 2024 - **Roberta Winston** - Initial release.

<hr>

## CURL Examples

### Login

```
curl -k -c cookies.txt -H "Content-Type: application/json" -X POST https://192.0.2.0/web/api/v1/login -d "{\"user\":\"myusername\",\"password\":\"mypassword\"}"
```

### Logout

```
curl -k -b cookies.txt -H "Content-Type: application/json" -X POST https://192.0.2.0/web/api/v1/logout
```

### Authentication

##### GET /v1/authentication/passwordPolicy
```
curl -k -b cookies.txt -X GET https://192.0.2.0/web/api/v1/authentication/passwordPolicy
```

##### GET /v1/authentication/sessions
```
curl -k -b cookies.txt -X GET https://192.0.2.0/web/api/v1/authentication/sessions
```

##### GET /v1/authentication/sessions/`<name>`
```
curl -k -b cookies.txt -X GET https://192.0.2.0/web/api/v1/authentication/sessions/admin
```

##### GET /v1/authentication/sessionPolicy
```
curl -k -b cookies.txt -X GET https://192.0.2.0/web/api/v1/authentication/sessionPolicy
```

##### GET /v1/authentication/userAccounts
```
curl -k -b cookies.txt -X GET https://192.0.2.0/web/api/v1/authentication/userAccounts
```

##### GET /v1/authentication/userAccounts/`<name>`
```
curl -k -b cookies.txt -X GET https://192.0.2.0/web/api/v1/authenticatiion/userAccounts/myusername
```

##### POST /v1/authentication/passwordPolicy/factoryReset
```
curl -k -b cookies.txt -X POST https://192.0.2.0/web/api/v1/authentication/passwordPolicy/factoryReset
```

<!-- future
##### POST /v1/authentication/sessions/`<name>`/disconnect
```
curl -k -b cookies.txt -H "Content-Type: application/json" -X POST https://192.0.2.0/web/api/v1/authentication/sessions/anotherusername/disconnect -d "{\"reason\":\"Need to use the library.\"}"
```
-->

##### PUT /v1/authentication/sessionPolicy {"autoLogout": `<minutes|null>`, "autoIMCLogin": `<enabled"|"disabled">`}
```
curl -k -b cookies.txt -H "Content-Type: application/json" -X PUT https://192.0.2.0/web/api/v1/authentication/sessionPolicy -d "{\"autoLogout\": 1}"
```
```
curl -k -b cookies.txt -H "Content-Type: application/json" -X PUT https://192.0.2.0/web/api/v1/authentication/sessionPolicy -d "{\"autoIMCLogin\": \"disabled\"}"
```

##### POST /v1/authentication/userAccounts
```
curl -k -b cookies.txt -H "Content-Type: application/json" -X POST https://192.0.2.0/web/api/v1/authentication/userAccounts -d "{\"name\":\"<name>\", \"role\":\"Administrator\", \"email\":\"username@example.com\", \"password\":\"mypassword\", \"expirePassword\": \"no\"}"
```

<!-- future
##### PUT /v1/authentication/userAccounts/`<name>` 
```
curl -k -b cookies.txt -H "Content-Type: application/json" -X POST https://192.0.2.0/web/ap/v1/authentication/userAccounts/myUsername -d "{\"role\":\"Administrator\", \"email\":\"myusername@example.com\"}"
```
##### POST /v1/authentication/userAccounts/`<name>`/unlock
```
curl -k -b cookies.txt -H "Content-Type: application/json" -X POST https://192.0.2.0/web/api/v1/authentication/userAccounts/myusername/unlock
```
-->

##### POST /v1/authentication/userAccounts/`<name>`/setPassword
```
curl -k -b cookies.txt -H "Content-Type: application/json" -X POST https://192.0.2.0/web/api/v1/authentication/userAccounts/admin/setPassword -d "{\"password\":\"mypassword\", \"expirePassword\": \"yes\"}"
```

### Accessors (TS4500 only)

##### GET /v1/accessors
```
curl -k -b cookies.txt -X GET https://192.0.2.0/web/api/v1/accessors
```

##### GET /v1/accessors/`<location>`
```
curl -k -b cookies.txt -X GET https://192.0.2.0/web/api/v1/accessors/accessor_Aa
```
```
curl -k -b cookies.txt -X GET https://192.0.2.0/web/api/v1/accessors/accessor_Ab
```

##### PUT /v1/accessors/`<location>` {"velocityScalingXY": `<value>`, "velocityScalingPivot": `<value>`}
```
curl -k -b cookies.txt -X GET https://192.0.2.0/web/api/v1/accessors/accessor_Aa -d "{\"velocityScalingXY\": 60, \"velocityScalingPivot\": 80}
```

### Cleaning Cartridges

#### GET/v1/cleaningCartridges
```
curl -k -b cookies.txt -X GET https://192.0.2.0/web/api/v1/cleaningCartridges
```

#### GET /v1/cleaningCartridges/`<volser>`
```
curl -k -b cookies.txt -X GET https://192.0.2.0/web/api/v1/cleaningCartridges/CLNU87L9
```

#### GET /v1/cleaningCartridges/`<internalAddress>`
```
curl -k -b cookies.txt -X GET https://192.0.2.0/web/api/v1/cleaningCartridges/FF0400
```

### Data cartridges

###### GET /v1/dataCartridges
```
curl -k -b cookies.txt -X GET https://192.0.2.0/web/api/v1/dataCartridges
```

###### GET /v1/dataCartridges/`<internalAddress>`
```
curl -k -b cookies.txt -X GET https://192.0.2.0/web/api/v1/dataCartridges/FF0412
```

##### GET /v1/dataCartridges/`<volser>`
```
curl -k -b cookies.txt -X GET https://192.0.2.0/web/api/v1/dataCartridges/IBM011LT
```

##### GET /v1/dataCartridges/lifetimeMetrics
```
curl -k -b cookies.txt -X GET https://192.0.2.0/web/api/v1/dataCartridges/lifetimeMetrics
```

##### GET /v1/dataCartridges/`<internalAddress>`/lifetimeMetrics
```
curl -k -b cookies.txt -X GET https://192.0.2.0/web/api/v1/dataCartridges/FF0412/lifetimeMetrics
```

##### GET /v1/dataCartridges/`<volser>`/lifetimeMetrics
```
curl -k -b cookies.txt -X GET https://192.0.2.0/web/api/v1/dataCartridges/IBM%2011LT/lifetimeMetrics
```

### Diagnostic cartridges

##### GET /v1/diagnosticCartridges

```
curl -k -b cookies.txt -X GET https://192.0.2.0/web/api/v1/diagnosticCartridges
```

##### GET /v1/diagnosticCartridges/`<volser>`

```
curl -k -b cookies.txt -X GET https://192.0.2.0/web/api/v1/diagnosticCartridges/IBM011LT
```

##### GET /v1/diagnosticCartridges/`<internalAddress>`
```
curl -k -b cookies.txt -X GET https://192.0.2.0/web/api/v1/diagnosticCartridges/FF0412
```

##### GET /v1/diagnosticCartridges/lifetimeMetrics
```
curl -k -b cookies.txt -X GET https://192.0.2.0/web/api/v1/diagnosticCartridges/lifetimeMetrics
```

##### GET /v1/diagnosticCartridges/`<internalAddress>`/lifetimeMetrics
```
curl -k -b cookies.txt -X GET https://192.0.2.0/web/api/v1/diagnosticCartridges/FF0412/lifetimeMetrics
```

##### GET /v1/diagnosticCartridges/`<volser>`/lifetimeMetrics
```
curl -k -b cookies.txt -X GET https://192.0.2.0/web/api/v1/diagnosticCartridges/IBM011LT/lifetimeMetrics
```

### Drives

##### GET /v1/drives
```
curl -k -b cookies.txt -X GET https://192.0.2.0/web/api/v1/drives
```

##### GET /v1/drives/`<location>`
```
curl -k -b cookies.txt -X GET https://192.0.2.0/web/api/v1/drives/drive_F1C3R2
```

##### GET /v1/drives/`<sn>`
```
curl -k -b cookies.txt -X GET https://192.0.2.0/web/api/v1/drives/607BBFFFF8
```

##### POST /v1/drives/`<location>`/clean
```
curl -k -b cookies.txt -X GET https://192.0.2.0/web/api/v1/drives/drive_F1C3R2
```

##### POST /v1/drives/`<sn>`/clean
```
curl -k -b cookies.txt -H "Content-Type: application/json" -X POST https://192.0.2.0/web/api/v1/drives/607BBFFFF8/clean
```

##### PUT /v1/drives/`<location>` {"use": `<"access" | "controlPath" | "verification">`}
```
curl -k -b cookies.txt -H "Content-Type: application/json" -X PUT https://192.0.2.0/web/api/v1/drives/drive_F1C2R4 -d "{\"use\":\"access\"}"
```
```
curl -k -b cookies.txt -H "Content-Type: application/json" -X PUT https://192.0.2.0/web/api/v1/drives/drive_F1C2R4  -d "{\"use\":\"controlPath\"}"
```
```
curl -k -b cookies.txt -H "Content-Type: application/json" -X PUT https://192.0.2.0/web/api/v1/drives/drive_F1C2R4 -d "{\"use\":\"verification\"}"
```

##### PUT /v1/drives/`<sn>` {"use": `<"access" | "controlPath" | "verification">`}
```
curl -k -b cookies.txt -H "Content-Type: application/json" -X PUT  https://192.0.2.0/web/api/v1/drives/607BBFFFF8 -d "{"use":\"access"\"}"
```
```
curl -k -b cookies.txt -H "Content-Type: application/json" -X PUT  https://192.0.2.0/web/api/v1/drives/607BBFFFF8 -d "{"use":\"controlPath\"}"
```
```
curl -k -b cookies.txt -H "Content-Type: application/json" -X PUT  https://192.0.2.0/web/api/v1/drives/607BBFFFF8 -d "{"use":\"verification\"}"
```

##### POST /v1/drives/`<location>`/reset {"mode": `<"normal" | "hard">`} 
```
curl -k -b cookies.txt -H "Content-Type: application/json" -X POST https://192.0.2.0/web/api/v1/drives/drive_F1C2R2/reset -d "{\"mode\":\"hard\"}"
```
```
curl -k -b cookies.txt -H "Content-Type: application/json" -X POST https://192.0.2.0/web/api/v1/drives/drive_F1C2R2/reset -d "{\"mode\":\"normal\"}"
```

##### POST /v1/drives/`<sn>`/reset {"mode": `<"normal" | "hard">`}
```
curl -k -b cookies.txt -H "Content-Type: application/json" -X POST https://192.0.2.0/web/api/v1/drives/607BBFFFF8/reset -d "{\"mode\":\"hard\"}"
```
```
curl -k -b cookies.txt -H "Content-Type: application/json" -X POST https://192.0.2.0/web/api/v1/drives/607BBFFFF8/reset -d "{\"mode\":\"normal\"}"
```

##### PUT /v1/drives/`<location>` {"beacon": `<"enabled" | "disabled">`}
```
curl -k -b cookies.txt -H "Content-Type: application/json" -X POST https://192.0.2.0/web/api/v1/drives/drive_F1C2R2 -d "{\"beacon\":\"disabled\"}"
```
```
curl -k -b cookies.txt -H "Content-Type: application/json" -X POST https://192.0.2.0/web/api/v1/drives/drive_F1C2R2 -d "{\"beacon\":\"enabled\"}"
```

##### PUT /v1/drives/`<sn>` {"beacon": `<"enabled" | "disabled">`}
```
curl -k -b cookies.txt -H "Content-Type: application/json" -X POST https://192.0.2.0/web/api/v1/drives/607BBFFFF8 -d "{\"beacon\":\"disabled\"}"
```
```
curl -k -b cookies.txt -H "Content-Type: application/json" -X POST https://192.0.2.0/web/api/v1/drives/607BBFFFF8 -d "{\"beacon\":\"enabled\"}"
```

### Ethernet ports

##### GET /v1/ethernetPorts
```
curl -k -b cookies.txt -X GET https://192.0.2.0/web/api/v1/ethernetPorts
```

##### GET /v1/ethernetPorts/`<location>`
```
curl -k -b cookies.txt -X GET https://192.0.2.0/web/api/v1/ethernetPorts/ethernetPort_F1Pa
```

##### PUT /v1/ethernetPorts/{location} {"ipv4Address": `<IPv4 address>`, "ipv4Subnet": `<IPv4 subnet mask>`, "ipv4Gateway": `<IPv4 gatway address>`, "ipv4Assignment": `<"static"|"dynamic">`, "ipv4Primary": `<IPv4 address>`, "ipv4Secondary": `<IPv4 address>`}

```
curl -k -b cookies.txt -H "Content-Type: application/json" -X PUT https://192.0.2.0/web/api/v1/ethernetPorts/ethernetPort_F1Pa -d "{\"ipv4Assignment\": \"static\", \"ipv4Address\": \"192.0.2.2\", \"ipv4Subnet\": \"255.255.252.0\", \"ipv4Gateway\": \"192.0.2.24\"}"
```

### Events

##### GET /v1/events
```
curl -k -b cookies.txt -X GET https://192.0.2.0/web/api/v1/events
```

##### GET /v1/events/`<ID>`
```
curl -k -b cookies.txt -X GET https://192.0.2.0/web/api/v1/events/876
```

##### GET /v1/events/`<ID>`/fixProcedure
```
curl -k -b cookies.txt -X GET https://192.0.2.0/web/api/v1/events/1038/fixProcedure
```

### Fibre Channel ports

##### GET /v1/fcPorts
```
curl -k -b cookies.txt -X GET https://192.0.2.0/web/api/v1/fcPorts
```

##### GET /v1/fcports/`<location>`
```
curl -k -b cookies.txt -X GET https://192.0.2.0/web/api/v1/fcports/fcPort_F1C1R4P0
```

 
### Frames

##### GET /v1/frames
```
curl -k -b cookies.txt -X GET https://192.0.2.0/web/api/v1/frames
```

##### GET /v1/frames/`<location>`
```
curl -k -b cookies.txt -X GET https://192.0.2.0/web/api/v1/frames/frame_F1
```
 
### GUI settings

##### GET /v1/guiSettings
```
curl -k -b cookies.txt -X GET https://192.0.2.0/web/api/v1/guiSettings
``` 

### I/O stations

##### GET /v1/ioStations
```
curl -k -b cookies.txt -X GET https://192.0.2.0/web/api/v1/ioStations
```

##### GET /v1/iostations/`<location>`
```
curl -k -b cookies.txt -X GET https://192.0.2.0/web/api/v1/iostations/ioStation_C3
```

 
### Library

##### GET /v1/library
```
curl -k -b cookies.txt -X GET https://192.0.2.0/web/api/v1/library
```

##### POST /v1/library/reset
```
curl -k -b cookies.txt -H "Content-Type: application/json" -X POST https://192.0.2.0/web/api/v1/library/reset 
```

##### PUT /v1/library
```
curl -k -b cookies.txt -X GET https://192.0.2.0/web/api/v1/library -d "{\"time\":\"2024-10-20T22:46:00\"}"
```

##### PATCH /v1/library {"ntpMode": `<"enabled|"disabled">`, "primaryNtpAddress": `<address>`, "secondaryNtpAddress": `<address>`}
```
curl -k -b cookies.txt -H "Content-Type: application/json" -X POST https://192.0.2.0/web/api/v1/library -d "{\"ntpMode\": \"enabled\", \"primaryNtpAddress\": \"192.0.2.1\", \"secondaryNtpAddress\": \"192.0.2.1\"}"
```

##### PATCH /v1/library {"timezone": `<time zone>`}
```
curl -k -b cookies.txt -H "Content-Type: application/json" -X POST https://192.0.2.0/web/api/v1/library -d "{\"timezone\":\"America/Phoenix\"}"
```

##### PATCH /v1/library {"capacityUtilThresh": `<value>`}
```
curl -k -b cookies.txt -H "Content-Type: application/json" -X POST https://192.0.2.0/web/api/v1/library -d "{\"capacityUtilThresh\": 90.9}"
```

##### PATCH /v1/library {"location": `<install location description>`, "address": `<install address>`, "city": `<install city>`, "state": `<install state>`, "country": `<install country>`, "contact": `<library admin>`, "telephone": `<library admin phone>`, "secondaryTelephone": `<library admin backup phone>`}
```
curl -k -b cookies.txt -H "Content-Type: application/json" -X POST https://192.0.2.0/web/api/v1/library -d "{\"location\": \"Storage Lab\", \"address\": \"0 Main St\", \"city\": \"Phoenix\", \"state\": \"AZ\", \"country\": \"US\", \"contact\": \"J%20Doe\"}"
```

###### GET /v1/library/saveConfig 
```
curl -k -b cookies.txt -X GET https://192.0.2.0/web/api/v1/library/saveConfig --output dbfile.dbz
```

###### POST /v1/library/restoreConfig  
```
curl -k -v -b cookies.txt -H "Content-Type: multipart/form-data" POST https://192.0.2.0/web/api/v1/library/restoreConfig -F 'filename=@dbfile.dbz; type=application/octet-stream'
```

### Logs

##### GET /v1/logs
```
curl -k -b cookies.txt -X GET https://192.0.2.0/web/api/v1/logs
```

##### GET /v1/logs/`<filename>`
```
curl -k -b cookies.txt -X GET https://192.0.2.0/web/api/v1/logs/TS4500_LOG_FA004_20240507102856.zip
```

##### GET /v1/logs/`<filename>`/export
```
curl -k -b cookies.txt -X GET https://192.0.2.0/web/api/v1/logs/TS4500_LOG_FA004_20240507102856.zip/export
```

### Node cards

##### GET /v1/nodeCards
```
curl -k -b cookies.txt -X GET https://192.0.2.0/web/api/v1/nodeCards
```

##### GET /v1/nodeCards/`<ID>`
```
curl -k -b cookies.txt -X GET https://192.0.2.0/web/api/v1/nodeCards/65
```

##### POST /v1/nodeCards/`<ID>`/reset
```
curl -k -b cookies.txt -H "Content-Type: application/json" -X POST https://192.0.2.0/web/api/v1/nodeCards/65/reset
```

### Power supplies

##### GET /v1/powerSupplies
```
curl -k -b cookies.txt -X GET https://192.0.2.0/web/api/v1/powerSupplies
```

##### GET /v1/powerSupplies/`<location>`
```
curl -k -b cookies.txt -X GET https://192.0.2.0/web/api/v1/powerSupplies/powerSupply_F1PSa
```

 
### Logical libraries

##### GET /v1/logicalLibraries
```
curl -k -b cookies.txt -X GET https://192.0.2.0/web/api/v1/logicalLibraries
```

##### GET /v1/logicalLibraries/`<name>`
```
curl -k -b cookies.txt -X GET https://192.0.2.0/web/api/v1/logicalLibraries/BackupLib
```

##### GET /v1/logicalLibraries/`<name>`/voslerRanges
```
curl -k -b cookies.txt -X GET https://192.0.2.0/web/api/v1/logicalLibraries/LogicalLibrary1/voslerRanges
```

##### POST /v1/logicalLibraries/'<name>`/volserRanges {"start": `<starting VOLSER>`, "end": `<ending VOLSER>`, "applyNow": `<"yes"|"no">`}
```
curl -k -b cookies.txt -H "Content-Type: application/json" -X POST https://192.0.2.0/web/api/v1/logicalLibraries/LogLib_1/volserRanges -d "{\"start\": \"AAA000\", \"end\": \"BBB000\", \"applyNow\": \"yes\"}"
```

##### POST /v1/logicalLibraries/`<name>`/assignDataCartridges {"cartridges": [`<VOLSER1|internalAddress1>`, `<VOLSER2|internalAddress2>` ...]}
```
curl -k -b cookies.txt -H "Content-Type: application/json" -X POST https://192.0.2.0/web/api/v1/logicalLibraries/LogLib_1/volserRanges -d "{\"cartridges\": [\"AAA001\", \"AAA002\"]}"
```

##### POST /v1/logicalLibraries/`<name>`/unassignDataCartridges {"cartridges": [`<VOLSER1|internalAddress1>, `<VOLSER2|internalAddress2>` ...]}
```
curl -k -b cookies.txt -H "Content-Type: application/json" -X POST https://192.0.2.0/web/api/v1/logicalLibraries/Lib1/unassignDataCartridges -d "{\"cartridges\": [\"AAA001\", \"AAA002\"]}"
```

##### POST /v1/logicalLibraries/`<name>`/assignDrives {"drives": [`<locationOrSN|sn>`, ...]}
```
curl -k -b cookies.txt -H "Content-Type: application/json" -X POST https://192.0.2.0/web/api/v1/logicalLibraries/LogLib_3/assignDrives -d "{\"drives\": \"drive_F1C2R4\"}"
```

##### POST /v1/logicalLibraries/`<name>`/unassignDrives {"drives": [`<locationOrSN|sn>`, ...]}
```
curl -k -b cookies.txt -H "Content-Type: application/json" -X POST https://192.0.2.0/web/api/v1/logicalLibraries/{name}/unassignDrives  -d "{\"drives\": \"1013000276\"}"
```
##### POST /v1/logicalLibraries/`<name>`/configureEncryption {"method": `<encryption method>`}
```
curl -k -b cookies.txt -H "Content-Type: application/json" -X POST https://192.0.2.0/web/api/v1/logicalLibraries/{name}/configureEncryption -d "{\"method\": \"applicationManaged\"}"
```
##### POST /v1/logicalLibraries {"name": <LL name>, "drives": {`<locationOrSN|sn>`, ...], "mediaType": `<LTO"|"3592">`}
```
curl -k -b cookies.txt -H "Content-Type: application/json" -X POST https://192.0.2.0/web/api/v1/logicalLibraries -d "{\"name\": \"Library_A\", \"drives\": [{\"drive_F1C2R4\", \"1013000276\"], \"mediaType\": \"LTO\"}"
```

##### GET /v1/logicalLibraries
```
curl -k -b cookies.txt -H "Content-Type: application/json" -X POST https://192.0.2.0/web/api/v1/logicalLibraries
```

##### GET /v1/logicalLibraries/`<name>`
```
curl -k -b cookies.txt -H "Content-Type: application/json" -X POST https://192.0.2.0/web/api/v1/logicalLibraries/Library_A 
```

##### GET /v1/logicalLibraries/`<name>`/voslerRanges
```
curl -k -b cookies.txt -H "Content-Type: application/json" -X POST https://192.0.2.0/web/api/v1/logicalLibraries/Library_A/volserRanges
```

##### PATCH /v1/logicalLibraries/`<name>` {"name": `<new name>`}
```
curl -k -b cookies.txt -H "Content-Type: application/json" -X POST https://192.0.2.0/web/api/v1/logicalLibraries/Library_A
```

### Reports

###### GET /v1/reports/accessors
```
curl -k -b cookies.txt -X GET https://192.0.2.0/web/api/v1/reports/accessors
```

###### GET /v1/reports/accessors?after=`<YYYY-MM-DDThh:mm:ss>`&before=`<YYYY-MM-DDThh:mm:ss>`
```
curl -k -b cookies.txt -X GET https://192.0.2.0/web/api/v1/reports/accessors%3Fafter=2024-06-12T10:00:00%26before=2024-06-12T12:00:00:00
```

###### GET /v1/reports/drives
```
curl -k -b cookies.txt -X GET https://192.0.2.0/web/api/v1/reports/drives
```

###### GET /v1/reports/drives?after=`<YYYY-MM-DDThh:mm:ss>`&before=`<YYYY-MM-DDThh:mm:ss>`
```
curl -k -b cookies.txt -X GET https://192.0.2.0/web/api/v1/reports/drives%3Fafter=2024-06-12T10:00:00%26before=2024-06-12T12:00:00:00
```

###### GET /v1/reports/library
```
curl -k -b cookies.txt -X GET https://192.0.2.0/web/api/v1/reports/library
```

###### GET /v1/reports/library?after=`<YYYY-MM-DDThh:mm:ss>`&before=`<YYYY-MM-DDThh:mm:ss>`
```
curl -k -b cookies.txt -X GET https://192.0.2.0/web/api/v1/reports/library%3Fafter=2024-06-12T10:00:00%26before=2024-06-12T12:00:00:00
```

 
### Slots and Tiers

##### GET /v1/slots
```
curl -k -b cookies.txt -X GET https://192.0.2.0/web/api/v1/slots
```

##### GET /v1/slots/`<location>`
```
curl -k -b cookies.txt -X GET https://192.0.2.0/web/api/v1/slots/slot_F1C4R8
```
 

 
### Tasks

##### GET /v1/tasks
```
curl -k -b cookies.txt -X GET https://192.0.2.0/web/api/v1/tasks
```

##### GET /v1/tasks/`<ID>`
```
curl -k -b cookies.txt -X GET https://192.0.2.0/web/api/v1/tasks/82
```

##### POST /v1/tasks {"type": "inventoryTier0and1", "location": `<"library" | "frame_F`<f>`">`}
```
curl -k -b cookies.txt -H "Content-Type: application/json" -X POST https://192.0.2.0/web/api/v1/tasks -d "{\"type\":\"inventoryTier0and1\", \"location\":\"library\"}"
```

##### POST /v1/tasks [{"type": "inventoryAllTiers", "location": `<"library" | "frame_F`<f>`">`}]
```
curl -k -b cookies.txt -H "Content-Type: application/json" -X POST https://192.0.2.0/web/api/v1/tasks -d "{\"type\":\"inventoryAllTiers\", \"location\":\"library\"}"
```

##### POST /v1/tasks {"type": "startDriveService", "location": "drive_F`<f>`C`<c>`R`<r>`"}
```
curl -k -b cookies.txt -H "Content-Type: application/json" -X POST https://192.0.2.0/web/api/v1/tasks -d "{\"type\":\"startDriveService\", \"location\":\"drive_F1C3R5\"}"
```

##### POST /v1/tasks {"type": "completeDriveService", "location": "drive_F`<f>`C`<c>`R`<r>`"}
```
curl -k -b cookies.txt -H "Content-Type: application/json" -X POST https://192.0.2.0/web/api/v1/tasks -d "{\"type\":\"completetDriveService\", \"location\":\"drive_F1C3R5\"}"
```

##### POST /v1/tasks {"type": "calibrateLibrary", "accessor": "accessor_A`<a|b>`"} 
```
curl -k -b cookies.txt -H "Content-Type: application/json" -X POST https://192.0.2.0/web/api/v1/tasks -d "{\"type\":\"calibrateLibrary\", \"accessor\":\"accessor_Aa\"}"
```

##### POST /v1/tasks {"type": "calibrateFrame", "location": "frame_F`<f>`", "accessor": "accessor_A`<a|b>`"} (TS4500 only)
```
curl -k -b cookies.txt -H "Content-Type: application/json" -X POST https://192.0.2.0/web/api/v1/tasks -d "{\"type\":\"calibrateFrame\", \"location\":\"frame_F1\", \"accessor\": \"accessor_Aa\"}"
```

##### POST /v1/tasks {"type": "calibrateAccessor", "accessor": "accessor_A`<a|b>`"} (TS4500 only)
```
curl -k -b cookies.txt -H "Content-Type: application/json" -X POST https://192.0.2.0/web/api/v1/tasks -d "{\"type\":\"calibrateAccessor\", \"accessor\":\"accessor_Aa\"}"
```

##### POST /v1/tasks testDrive {"type": "testDrive", "location": "drive_F`<f>`C`<c>`R`<r>`"}
```
curl -k -b cookies.txt -H "Content-Type: application/json" -X POST https://192.0.2.0/web/api/v1/tasks -d "{\"type\":\"testDrive\", \"location\": \"drive_F1C5R3\"}"
```

##### POST /v1/tasks testDrive {"type": "updateLibraryFirmware"}
```
curl -k -b cookies.txt -H "Content-Type: multipart/form-data" POST https://192.0.2.0/web/api/v1/tasks -F "filename=@TS4500_11100-05G.afwz; type=application/octet-stream" -F "{\"type\": \"updateLibraryFirmware\"}; type= application/json"
```

##### POST /v1/tasks testDrive {"type": "updateDriveFirmware", "drive_F`<f>`C`<c>`R`<r>`"}
```
curl -k -b cookies.txt -H "Content-Type: multipart/form-data" POST https://192.0.2.0/web/api/v1/tasks -F "filename=@D3I4_A0B.fcp_fj_D.fmrz; type=application/octet-stream" -F "{\"type\": \"updateDriveFirmware\", \"location\":\"drive_F1C4R4\"}; type= application/json"
```


 

### Roles

##### GET /v1/authentication/roles
```
curl -k -b cookies.txt -X GET https://192.0.2.0/web/api/v1/authentication/roles
```

##### GET /v1/authentication/roles/`<name>`
```
curl -k -b cookies.txt -X GET https://192.0.2.0/web/api/v1/authentication/roles/Administrator
```
 
### Syslog notifications

##### GET /v1/notification/syslog/servers
```
curl -k -b cookies.txt -X GET https://192.0.2.0/web/api/v1/notification/syslog/servers
```

##### GET /v1/notification/syslog/servers/`<ipAddress>`
```
curl -k -b cookies.txt -X GET https://192.0.2.0/web/api/v1/notification/syslog/servers/192.0.2.11
```

##### POST /v1/notification/syslog/servers {"address": `<address>`, "port": `<port>`, "subscribed": ["error"|"warning"|"information", ...]}
```
curl -k -b cookies.txt -H "Content-Type: application/json" -X POST https://192.0.2.0/web/api/v1/notification/syslog/servers -d "{\"address\": \"192.0.2.11\", \"port\": \"514\", \"subscribed\": \"error\"}"
```

##### GET /v1/notification/syslog/servers
```
curl -k -b cookies.txt -X GET https://192.0.2.0/web/api/v1/notification/syslog/servers
```

##### GET /v1/notification/syslog/servers/`<address>`
```
curl -k -b cookies.txt -X GET https://192.0.2.0/web/api/v1/notification/syslog/servers/192.0.2.11
```

##### PUT /v1/notification/syslog/servers/`<address>` {"address": `<address>`, "port": <port>}
```
curl -k -b cookies.txt -H "Content-Type: application/json" -X POST https://192.0.2.0/web/api/v1/notification/syslog/servers/192.0.2.9 -d "{\"address\": \"192.0.2.10\", \"port\": \"514\"}"
```

##### PUT /v1/notification/syslog/servers/`<address>` {"subscribed": ["information" | "warning" | "error", ...]}
```
curl -k -b cookies.txt -H "Content-Type: application/json" -X POST https://192.0.2.0/web/api/v1/notification/syslog/servers/192.0.2.10 -d "{\"subscribed\": \"information\"}"
```

### Work items
```
curl -k -b cookies.txt -X GET https://192.0.2.0/web/api/v1/workItems
```
##### POST /v1/workItems {"type": "moveToSlot", "cartridge": `<volser>`,"sourceInternalAddress": `<internalAddress>`, "destinationLocation": `<location>`}
```
curl -k -b cookies.txt -H "Content-Type: application/json" -X POST https://192.0.2.0/web/api/v1/workItems -d "{\"type\": \"moveToSlot\", \"cartridge\": \"FF0006L8\", \"destinationLocation\": \"slot_F1C2R5T1\"}"
```

##### POST /v1/workItems [{"type": "moveToDrive", "cartridge": `<volser>`,"sourceInternalAddress": `<internalAddress>`, "destinationLocation": `<location>`, "destinationSN": `<serialNumber>`}]
```
curl -k -b cookies.txt -H "Content-Type: application/json" -X POST https://192.0.2.0/web/api/v1/workItems -d "{\"type\":\"moveToDrive\", \"cartridge\":\"FF0002L8\", \"destinationLocation\": \"drive_F1C2R2\"}"

```

##### POST /v1/workItems [{"type": "moveToIOStation", "cartridge": `<volser>`, "sourceInternalAddress": `<internalAddress>`, "destinationLocation": `<location>`}]
```
curl -k -b cookies.txt -H "Content-Type: application/json" -X POST https://192.0.2.0/web/api/v1/workItems -d "{\"type\":\"moveToIOStation\", \"sourceInternalAddress\":\"010404\", \"destinationLocation\": \"ioSlot_C3R2T1\"}"
```






