# Optimization of LTO-9 cartridges
[Media optimzation](https://www.ibm.com/docs/en/t-tt-and-t?topic=introduction-media-optimization) is a new feature for the LTO-9 tape drive.

ITDT (IBM Tape Diagnostic Tool) supports the media optimization.

## 1. Obtain the latest version of ITDT-SE (Standard Edition)
ITDT is available for different platforms and can be downloaded from IBM FixCentral free of charge.
To obtain ITDT:
- Access IBMfixCentral: https://www.ibm.com/support/fixcentral
- Enter 'ITDT' in the product selector and select the 'IBM Tape Diagnostic Tool ITDT'
- Choose you operating system and press continue
- Download the ITDT install package, e.g. `itdtinst9.6.1.20230511inuxX86_64`
- Install the package

## 2.1 Media Optimzation for non IBM tape libraries
The Unix script `loadCartridges.sh` is intended to automate cartridge initialization in an library environment.
It utilizes the ITDT (IBM Tape Diagnostic Tool) Tool scripting commands to mount and unmount cartridges.

Copy the script `loadCartridges.sh`in the `ITDT` installation folder. The script can be 
started. Without any parameters, the usage screen is showing the available parameters.

<sub>++++++++++++++++Usage Information++++++++++++++++++++++++++++++++++ <br>
Usage: ./loadCartridges.sh [OPTIONS] devicename [changername] <br>
  where devicename/changername is an IBMTapeDeviceName (like /dev/IBMTape0) <br>
  or a Linux generic SCSI device (/dev/sg1) <br>
  To determinate the correct device names, please use ./itdt scan <br>
   <br>  <br>
 Options: <br>
  --start number       first storage location used for inventory <br>
  --slots number       number of storage locations used for inventory <br>
  --unattended         unattended mode <br>
  --help               show usage information <br>
</sub>


## 2.2 Media Optimization for IBM tape libraries
With ITDT-SE 9.6.1 a new scripting parameter `librarymediaoptimization` was introduced.

The `librarymediaoptimization` subcommand for medium changers offers the option to identify uninitialized cartridges in a logical tape library and load cartridges in the
desired tape drive(s) for optimization.

Syntax: librarymediaoptimization [-start number] [-slots numberofslots] [-drives numberofdrives] [-drivelist identifiers]

Parameters: \
-start number: \
  number should specify the first storage element address which should be used for the media optimization.\
  default: first storage element address\
\
-slots numberofslots: \
  numberofslots specifies the number of cartridges which should be used for the media optimization.\
  default: number of storage elements \
\
-drives numberofdrives: \
  numberofdrives specifies the maximum number of drives used for the optimization.\
  default: all drives are used\
  \
-drivelist identifier(s): \
  identifiers is a comma separated list containing the drive element address or the drive serial number\
  default: all drives are used\

<br>
If none of the optional parameters is specified all available drives and all storage slots are used for media optimization.

Examples:
<code>
  ./itdt -f /dev/IBMChanger0 librarymediaoptimization
  ./itdt -f /dev/IBMChanger0 librarymediaoptimization -slots 10 -drives 256,257
  ./itdt -f /dev/sg7 librarymediaoptimization -start 4096 -slots 10
  ./itdt -f /dev/sg7 librarymediaoptimization –drivelist 01234567890,0123456789A
</code>


