#!/bin/bash
#################################################################################
#  Licensed Materials - Property of IBM                                         #
#                                                                               #
#  Automated process used to get drive dumps                                    #
#                                                                               #
#  (C) Copyright IBM Corp. 2022 All Rights Reserved.                            #
#                                                                               #
# US Government Users Restricted Rights - Use, duplication or                   #
# disclosure restricted by GSA ADP Schedule Contract with IBM Corp.             #
#                                                                               #
# This script was developed by IBM Technical Services, Kelsterbach Germany      #
#################################################################################
set -u

#VARIABLES
PROGRAM_VERSION=1.0.0
ITDT=./itdt
    
#################################################################################
#
# show usage information
#
#################################################################################
usage()
{
    echo ""
    echo "++++++++++++++++Usage Information++++++++++++++++++++++++++++++++++" 
    echo "Usage: ${0} [OPTIONS] devicename [changername]"
    echo "  where devicename/changername is an IBMTapeDeviceName (like /dev/IBMTape0)"
    echo "  or a Linux generic SCSI device (/dev/sg1)"
    echo "  To determinate the correct device names, please use ./itdt scan"
    echo ""
    echo " Options:"
    echo "  --start number       first storage location used for inventory"
    echo "  --slots number       number of storage locations used for inventory"
    echo "  --unattended         unattended mode"
    echo "  --help               show usage information"
    echo ""
    echo "Program version: ${PROGRAM_VERSION}"
}

#################################################################################
#
# load one after the other cartridge and perform read dump command
#
#################################################################################
loadCartridges()
{
    echo "++++++!!!!!+++++Load Cartridges+++++++++++++++++++++!!!!!+++++++" | tee -$LOG_FILE
    echo `date` >> $LOG_FILE
    count="0"
    
    for slot in $VOLSER_ADDR
    do 
        echo "${ITDT} -f $CHANGER move ${array_addr[$count]} $DRIVE_ADDRESS" | tee -a $LOG_FILE
		${ITDT} -f $CHANGER move ${array_addr[$count]} $DRIVE_ADDRESS | tee -a $LOG_FILE

        ## Clear unit attention condition
        ${ITDT} -f $DRIVE tur  > /dev/null 2>&1
        ${ITDT} -f $DRIVE tur  | tee -a $LOG_FILE
        ${ITDT} -f $DRIVE load | tee -a $LOG_FILE
        for retry in {1..40}
        do
        	${ITDT} -f $DRIVE tur  | tee -a $LOG_FILE
        	if [ "$?" -eq 0 ]; then
        		break
        	fi
        	sleep 60
		done

        echo "${ITDT} -f $DRIVE unload " | tee -a $LOG_FILE
        ${ITDT} -f $DRIVE unload | tee -a $LOG_FILE
        echo "${ITDT} -f $CHANGER move $DRIVE_ADDRESS ${array_addr[$count]}" | tee -a $LOG_FILE
        ${ITDT} -f $CHANGER move $DRIVE_ADDRESS ${array_addr[$count]} | tee -a $LOG_FILE
        count=`expr $count + 1`
    done
    echo "++++++++++++++++++++Done+++++++++++++++++++++++++++++++++++++++++++" | tee -a $LOG_FILE
 
}

#################################################################################
#
# check prerequisites, root access and ITDT
#
#################################################################################
checkPrerequisites()
{
	echo "++++++++++++++++Check Prerequisites++++++++++++++++++++++++++++++++"
    if [ ! -e ${ITDT} ]; then
		echo "!!!!Error: Failed to locate itdt, please run the script in ITDT's folder.!!!!"
		exit 7
    fi
	
	if [ "$(id -u)" != "0" ]; then
		echo "!!!!Error: This script must be run as root.!!!!" 1>&2
		exit 9
	fi
}   
#################################################################################
#
# at program start up unload cartridge form speficied tape device
#
#################################################################################
unloadDrive()
{
    echo "++++++++++++++++Drive Status+++++++++++++++++++++++++++++++++++++++"
    SOURCEADDR=`${ITDT} -f $CHANGER devid | grep -A 7 "Drive Address ${DRIVE_ADDRESS}" | grep "Media Present" | awk '{ print $4}'`
    if [ "$SOURCEADDR" == "Yes" ]; then
	SOURCEADDR=`${ITDT} -f $CHANGER devid | grep -A 7 "Drive Address ${DRIVE_ADDRESS}" | grep "Source Element Address \." | awk '{ print $5}'`
        echo " Cartridge in drive loaded $SOURCEADDR "
        echo " Drive addr $DRIVE_ADDRESS "
        ${ITDT} -f $CHANGER move $DRIVE_ADDRESS $SOURCEADDR
    else
        echo "Drive is empty."
    fi
}


#################################################################################
#
# select menu, shown after inventory scan 
#
#################################################################################
selectFunction()
{
    if [ "$UNATTENDED" = "true" ]; then
        loadCartridges
    else
	valid="false"
	while [ "$valid" == "false" ];
	do
  	    echo "++++++?????+++++Select Function++++++++++++++++++++++++?????+++++++"
            echo "      [0]   Load Cartridges" 
            echo "      [1]   Quit" 
            echo -n "Please enter script index number: ";read function_index
            if [ "$function_index" -lt 2 ]; then
		valid="true" 
            else
		echo "++++++!!!!! Selected Function Number is not valid++++++!!!!!+++++++";    
            fi    
	done    
	if [ "$function_index" ==  1 ]; then
            echo "Quit script!";    
            finish="true"
	else
            loadCartridges            
	fi
    fi
}

#################################################################################
#
# read library inventory
#
#################################################################################
readLibraryInventory()
{
    echo "++++++++++++++++Changer Inventory++++++++++++++++++++++++++++++++++"
    LAST_SLOT=`expr $FIRST_SLOT + $NUMBER_OF_SLOTS`
    INDEX=$FIRST_SLOT
    while [ "$INDEX" -le "$LAST_SLOT" ]
    do
	VOLSER=`${ITDT} -f $CHANGER cartridge $INDEX | grep "Volume Tag" |awk '{print $4}'`
	MEDIA_PRESENT=`${ITDT} -f $CHANGER cartridge $INDEX | grep "Media Present" |awk '{print $4}'`

	if [ "$MEDIA_PRESENT" = "Yes" ]; then
            VOLSERLIST="$VOLSERLIST $VOLSER "
            VOLSER_ADDR="$VOLSER_ADDR $INDEX "
            echo "          Cartridge at Slot: $INDEX  Volser:$VOLSER "
	fi
	INDEX=`expr $INDEX + 1`
    done
    array_volser=($VOLSERLIST)
    array_addr=($VOLSER_ADDR)
    echo "Number of detected Cartridges            : ${#array_addr[*]}"
}

#################################################################################
#
# check commandline options 
#
#################################################################################
checkCommadlineParameter()
{
    if [ "$#" -eq 0 ]; then
	usage;
	exit
    fi
    DRIVE=""
    CHANGER=""
    START_SLOT_2_SET=""
    NUMBER_OF_SLOTS_2_SET=""
    UNATTENDED="false"
    VERIFY="false"
    while [ $# -ne 0 ]
    do
	arg="$1"
	case "$arg" in
            --start)
		shift
		START_SLOT_2_SET=$1
		;;
            --slots)
		shift
		NUMBER_OF_SLOTS_2_SET=$1
		;;
	    --unattended)
		UNATTENDED="true"
		;;
	    --help)
		usage
		exit 0;
		;;
	    -*)
		echo "!!!!Error: invalid option specified [$1].!!!!"
		exit 8;
		;;
            *)
                if [ -z $DRIVE ]; then
		    DRIVE=$1
                else
                    CHANGER=$1
                fi
		;;
	esac
	shift
    done
}

#################################################################################
#
# Global variables and System information
#
#################################################################################
readSystemConfiguration()
{
    echo "++++++++++++++++System Configuration+++++++++++++++++++++++++++++++"
    if [ ! -e ${ITDT} ]; then
        echo "!!!!Error: Failed to locate itdt, please run the script in ITDT's folder.!!!!"
        exit 7
    fi

    VOLSERLIST=""
    VOLSER_ADDR=""
    DRIVE_ADDRESS="0"
    ###### scan bus for connected devices to determinate driver changer assignment ##
    if [ -z $CHANGER ]; then
		SCAN=`${ITDT} scan -o "%D %C %S %V-%P H%H-B%B-T%T"`
		DRIVE_SCAN_RESULT=`echo "$SCAN" | grep "$DRIVE"`
		DRIVE_SN=`echo "$DRIVE_SCAN_RESULT" | awk '{print $3}'` 
		DRIVE_INQ=`echo "$DRIVE_SCAN_RESULT" | awk '{print $4}'`
		DRIVE_HBT=`echo "$DRIVE_SCAN_RESULT" | awk '{print $5}'`
    else
		DRIVE_SN=`${ITDT} -f ${DRIVE} inqj 0x83 | grep serialNumber | awk '{print $2}' | sed 's/\"//g'`
		DRIVE_INQ=`${ITDT} -f ${DRIVE} inqj 0x83 | grep vendorIdentification | awk '{print $2}' | sed 's/\"//g'`
		DRIVE_HBT='-1 -1 -1 -1'
    fi
    LOG_FILE=./${DRIVE_SN}.log
    RESULT_FILE=./${DRIVE_SN}.result
    if [ "$DRIVE_INQ" == ""  ]; then 
	echo "!!!!Error: Unable to determinate drive/changer association data!!!!"
	exit 1;
    fi
    ###### display system information to the console ###############################
    echo "Tape Drive Inquiry Data are              : $DRIVE_INQ"

    if [ "$DRIVE_SN" == ""  ]; then 
	echo "!!!!Error: Unable to determinate drive serialnumber!!!!"
	exit 2;
    fi
    echo "Tape Drive Serialnumber is               : $DRIVE_SN"

    if [ -z $CHANGER ]; then
		CHANGER_SN=`echo "$DRIVE_SCAN_RESULT" | awk -F ":" '{print $2}' | awk '{print $1}'`
        CHANGER=`${ITDT} scan -o "%D %S H%H-B%B-T%T" | grep "$CHANGER_SN"`
        COUNT=`echo "$CHANGER" | wc -l`
        if [ "$COUNT" == "0" ]; then 
	    echo "!!!!Error: Unable to determinate associated changer device!!!!"
	    exit 3;
        fi
        if [ "$COUNT" == "1" ]; then
            CHANGER=`echo $CHANGER | awk '{print $1}'`
        else
            echo "Multiple Controls Paths, select Path     : $DRIVE_HBT"
            CHANGER=`echo "$CHANGER" | grep "$DRIVE_HBT" | awk '{print $1}'`
        fi
    else
        echo "Use specified changer device             : $CHANGER"
		CHANGER_SN=`${ITDT} -f ${CHANGER} inqj 0x83 | grep serialNumber | awk '{print $2}' | sed 's/\"//g'`
    fi
    echo "Associated Changer device name is        : $CHANGER"
    echo "Associated Changer Serial Number is      : $CHANGER_SN"
    FIRST_SLOT=`${ITDT} -f $CHANGER eleminfo | grep "First Slot Address" |awk '{print $5}'`
    echo "Associated Changer First Slot address is : $FIRST_SLOT"
    NUMBER_OF_SLOTS=`${ITDT} -f $CHANGER eleminfo | grep "Number of Slots" |awk '{print $5}'`
    echo "Associated Changer Number of Slots       : $NUMBER_OF_SLOTS"
    LAST_SLOT=`expr $FIRST_SLOT + $NUMBER_OF_SLOTS`	
    ###### check if address range is specified ######################################
    if [ ! -z $START_SLOT_2_SET ]; then
	if [ "$START_SLOT_2_SET" -lt "$FIRST_SLOT" -o "$START_SLOT_2_SET" -gt "$LAST_SLOT" ]; then
	    echo "!!!!Error: Invalid First Slot $START_SLOT_2_SET specified!!!!"
	    exit 4;
	fi
	FIRST_SLOT=$START_SLOT_2_SET
	NUMBER_OF_SLOTS=`expr $LAST_SLOT - $FIRST_SLOT + 1`	
    fi
    if [ ! -z $NUMBER_OF_SLOTS_2_SET ]; then
	TMP=`expr $FIRST_SLOT + $NUMBER_OF_SLOTS_2_SET - 1`	
	if [ "$TMP" -gt "$LAST_SLOT" ]; then
	    echo "!!!!Error: Invalid amount of slots $NUMBER_OF_SLOTS_2_SET specified!!!!"
	    exit 5;
	fi
	NUMBER_OF_SLOTS=$NUMBER_OF_SLOTS_2_SET
    fi
    if [ "x$NUMBER_OF_SLOTS_2_SET" != "x" -o "x$START_SLOT_2_SET" != "x" ]; then
	echo "Inventory Range specifed First Slot      : $FIRST_SLOT"
	echo "Inventory Range specifed Number of Slots : $NUMBER_OF_SLOTS"
    fi

    DRIVE_ADDRESS=`${ITDT} -f $CHANGER devids  | grep -B 12 ${DRIVE_SN} | grep "Drive Address" |awk '{print $3}'`
    if [ "$DRIVE_ADDRESS" == "" ]; then 
	echo "!!!!Error: Unable to determinate drive address!!!!"
	exit 6;
    fi
    echo "Tape Drive Element Address is            : $DRIVE_ADDRESS"
    echo "Logfile is                               : $LOG_FILE"
}

###############################################################################
#                                                                             #
# Here starts main                                                            #
#                                                                             #
###############################################################################

###### check parameters #######################################################
checkCommadlineParameter "$@"

###### check prerequisites######################################################
checkPrerequisites

###### read and verify system configuration ###################################
readSystemConfiguration 

###### check status of tape drive , issue unload is a cartridge is loaded #####
unloadDrive

###### read library inventory #################################################
readLibraryInventory

###### show main selection dialog #############################################
selectFunction

