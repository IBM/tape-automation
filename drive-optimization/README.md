# Optimization of LTO-9 cartridges

The Unix script 'loadCartridges.sh' is intended to automate cartridge initialization in an library environment.
It utilizes the ITDT (IBM Tape Diagnostic Tool) Tool scripting commands to mount and unmount cartridges.

## Download ITDT
ITDT is available for different platforms and can be downloaded from IBM FixCentral free of charge.
To obtain ITDT:
- Access IBMfixCentral: https://www.ibm.com/support/fixcentral
- Enter 'ITDT' in the product selector and select the 'IBM Tape Diagnostic Tool ITDT'
- Choose you operating system and press continue
- Download the ITDT install package, e.g. `itdtinst9.6.0.20230215LinuxX86_64`
- Install the package

## Usage
After the script `loadCartridges.sh` is stored in the `ITDT` installation folder, the script can be 
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
