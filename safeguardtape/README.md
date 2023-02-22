


<!-- Name of the example script -->
# Safeguarded Tape

<!-- Description of what the example script does -->
## Description

An administrator can implement an air-gap solution for sensitive archival data to ensure it is kept physically offline to hosts without physical media handling.

  * **Air gap** - Data is physically offline to hosts and ISV applications
  * **Role-based access control** - Administrator intervention to bring it back online. 
  * **Physically inaccessible** - As today, media is locked in physical the library making them inaccessible to data center personnel.
  * **Automation** - As this script describes, this process can be fully automated by the administrator 
  * **Media verification** - Media verification can be enabled for media in the offline logical library

<!-- Description of how to use the script -->
## Usage

```
safeguardedtape.py --sourceLogicalLibrary xxx --targetLogicalLibrary
```

Arguments:

  * --sourceLogicalLibrary - Name of source logical library
  * --targetLogicalLibrary - Name of target logical library

The **safeguardedtape.py** script assumes the following:

  1. User has installed the [TS4500 CLI](https://www.ibm.com/docs/it/ts4500-tape-library?topic=commands-installing-cli) as a pre-requisite
  2. User provides a list of cartridges and logical library destinations in a txt file (Sample: filename.txt)
  3. User has both an online and offline [logical library](https://www.ibm.com/docs/en/ts4500-tape-library?topic=libraries-creating-logical) created 
  4. User provides a target logical library to be moved to (offline or online depending on the scenario)
  5. Where indicated '-ip' address is the IP address of the TS4500
  6. Where indicated '-u' user is a valid login for the TS4500 with Administrator role
  7. Where indicated '-p' user password for user
  8. This script is intended for end user customization, including template fields and is not expected to run as is.
  9. Offline logical library defined as a logical library with no (0) drives


<!-- Show product support information here -->
## Product Support

This script was designed for the [IBM TS4500 Tape Library](https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&cad=rja&uact=8&ved=2ahUKEwiIksKb6an9AhUjk2oFHXdiB8gQFnoECBUQAQ&url=https%3A%2F%2Fwww.ibm.com%2Fproducts%2Fts4500&usg=AOvVaw0d2vmUqVKsk3X_h3i3fpgf).  It was verified on firmware level [1.8.0.4-B00](https://www.ibm.com/support/fixcentral/swg/downloadFixes?parent=Tape%20autoloaders%20and%20libraries&product=ibm/Storage_Tape/TS4500+Tape+Library+(3584)&release=1.0&platform=All&function=fixId&fixids=TS4500_Tape_Library_Microcode_1.8.0.4_B00&includeRequisites=1&includeSupersedes=0&downloadMethod=http&login=true).

<!-- Change history includes data and one line saying what changed -->
## Change History

  * Feb 22, 2023 - **Melanie Dauber** - Initial release.


