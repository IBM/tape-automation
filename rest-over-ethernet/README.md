


<!-- Name of the example script -->
# REST over Ethernet

<!-- Description of what the example script does -->
## Description

A user can run REST over Ethernet requests using this script.
This can be run as a single request with a login and logout request surrounding it, or as an interactive session, allowing the user to enter one request after another.

When specifying an endpoint for the script, only the endpoint name should be used.

<!-- Description of how to use the script -->
## Usage

```
rest.py [-h] [-i IP] [-u USER] [-p PASSWORD] [-e ENDPOINT] [-j] [-s] [-n] [-r] [-m METHOD] [-jp PAYLOAD]
```

All arguments are optional. Anything necessary will be interactively queried at runtime.

rest.py Arguments:

  * **-h, --help**                        Show this help message and exit
  * **-i IP, --ip IP**                    IP address or hostname of library
  * **-u USER, --user USER**              Username for logging into the library
  * **-p PASSWORD, --password PASSWORD**  Password for logging into the library
  * **-e ENDPOINT, --endpoint ENDPOINT**  Specify a single endpoint to run against
  * **-j, --json**                        Performs basic JSON validation on the response
  * **-s, --showhttperror**               Shows the HTTP error code with the data
  * **-n, --noerror**                     Ignore any SSL errors
  * **-r, --nourl**                       Do not display the URL that is being queried
  * **-m METHOD, --method METHOD**        Default HTTP method for this request. POST, PUT, GET accepted.
  * **-jp PAYLOAD, --payload PAYLOAD**    JSON payload for requests.

safeguard.py Arguments:
  * **-h, --help**                        Show this help message and exit
  * **-i IP, --ip IP**                    IP address or hostname of library
  * **-u USER, --user USER**              Username for logging into the library
  * **-p PASSWORD, --password PASSWORD**  Password for logging into the library
  * **-s SOURCE_LL, --source SOURCE_LL**  Name of logical library that cartridges will be removed from
  * **-d DEST_LL, --destination DEST_LL** Name of logical library that cartridges will be moved to
  * **-c, --create**                      Flag to tell script that the destination logical library must be created
  * **-n, --noerror**                     Ignore any SSL errors
  * **-q, --quick**                       Flag to skip completion check after requests to reassign cartridges have completed

The **rest.py** script assumes the following:

  1. Where indicated '-ip' address is the IP address of the TS4500 or Diamondback
  2. Where indicated '-u' user is a valid login for the TS4500 or Diamondback
  3. Where indicated '-p' user password for user
  4. A user implementing this in production must edit the script to point the 'ca_file' variable to an actual certificate to utilize SSL


<!-- Show product support information here -->
## Product Support

This script was designed for the TS4500 and Diamondback tape libraries, and tested on code levels starting with 1.10.x.x and 2.10.x.x respectively.

<!-- Change history includes data and one line saying what changed -->
## Change History

  * Dec 28, 2023 - **Dylan Carlson** - Initial release.


