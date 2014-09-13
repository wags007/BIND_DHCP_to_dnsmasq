__author__ = 'bwagner'
import os
from ConfigParser import SafeConfigParser
from ScriptLog import log, log2, closeLog, error, warning, info, debug, entry, exit, lopen, handleException

try:
    config = SafeConfigParser()
    config.read( './Configuration/base.cfg' )
    logFileDir = str( config.get( "base", "logDir" ) )
    logFile = str( config.get( "base", 'dhcpTodnsmasqLogFile') )
    lopen( logFile, logFileDir )
    entry( "Entering dhcpTodnsmasq.init" )

    exit( "Exiting dhcpTodnsmasq.init" )
except:
    handleException( "dhcpTodnsmasq.init" )
    raise

class convertDhcpdTodnsmasqconf:

    def __init__ ( self ):
        pass

    def processDhcpdConfFile():
        entry("Opening DHCPD Config file")
        try:
            # Read the source dhcpd.conf configuration file
            dhcpConFileLocation = str( config.get("base","dhcpdConfigFile"))
            # Open the file
            dhcpConFile = open(dhcpConFileLocation,mode='r')
            # Read in the output directory
            dnsmasqConfDir = str(config.get("base","dnsmasqConfigDir"))
            # Read in the output file name
            dnsmasqDHCPFileName = str(config.get("base","dhcpDnsmasqConfFile"))
            # Check the path and create it if it doesn't exist
            if not os.path.isdir( dnsmasqConfDir ):
                log2( "Log directory %s does not exist" % dnsmasqConfDir)
                try:
                    os.mkdir( dnsmasqConfDir )
                except:
                    handleException( "Unable to create log directory" )
                    raise
            # Double check to make sure the directory exists
            if not os.path.isdir( dnsmasqConfDir ):
                log2("%s is not a directory" % dnsmasqConfDir)
                raise
            # Since it must certainly exist now let's make sure it's writable
            if not os.access( dnsmasqConfDir, os.W_OK ):
                print "Directory %s is not writable" % dnsmasqConfDir
                raise
            # Join the Directory and filename so that we can open the file for writing
            dnsmasqDHCPFile = os.path.join( dnsmasqConfDir , dnsmasqDHCPFileName )
            # While we have the file open for writing keep writing to it.  We use the with statement so if the
            # script crashes it will close the file cleanly first flushing the buffers.
            with open(dnsmasqDHCPFile,mode='w') as dnsmasqConf:
                #While we have the file open for reading and keep it open until we are done with it.
                with open(dhcpConFileLocation,mode='r') as dhcpConFile:
                    count = 0
                    for line in dhcpConFile:
                        # Look for Host Entries
                        if line.__contains__("host") and line.__contains__("{"):
                            splitline = line.split()
                            name = str(splitline[1])
                            count =count + 1
                        # Look for MAC Address
                        if line.__contains__("ethernet"):
                            splitline = line.split()
                            macaddress = str(splitline[2].strip(";"))
                        # Look for the assigned IP Address
                        if line.__contains__("fixed-address"):
                            splitline = line.split()
                            ipaddress = str(splitline[1].strip(";"))
                        # Look for the ending } and place the entry into the output file
                        if line.__contains__("}") and count > 0:
                            dnsmasqConf.write("dhcp-host=%s,%s,%s\n" % (name,macaddress,ipaddress))
                            count = 0
                        if line.__contains__("default-lease-time"):
                            maxLease = line.split()
                            dnsmasqConf.write("dhcp-lease-max=%s\n" % (maxLease[1].strip().strip(";")))
                        if line.__contains__("ntp-servers"):
                            ntpServers = line.split()
                            dnsmasqConf.write("dhcp-option=option:ntp-server,%s\n" % (ntpServers[2].strip(";")))
                        if line.__contains__("routes"):
                            routes = line.split()
                            dnsmasqConf.write("dhcp-option=121,%s/255.255.255.0" % (routes[2]))


        except:
            handleException("openDhcpdConfFile")
            raise

    processDhcpdConfFile()
