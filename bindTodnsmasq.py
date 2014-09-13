__author__ = 'bwagner'
import os
from ConfigParser import SafeConfigParser
from ScriptLog import log, log2, closeLog, error, warning, info, debug, entry, exit, lopen, handleException
import re

try:
    config = SafeConfigParser()
    config.read( './Configuration/base.cfg' )
    logFileDir = str( config.get( "base", "logDir" ) )
    logFile = str( config.get( "base", 'bindTodnsmasqLogFile') )
    lopen( logFile, logFileDir )
    entry( "Entering bindTodnsmasq.init" )

    exit( "Exiting bindTodnsmasq.init" )
except:
    handleException( "bindTodnsmasq.init" )
    raise

class convertBindTodnsmasqconf:

    def __init__ ( self ):
        pass

    def processBindNamedconfFile( ):
        entry("Opening named.conf Config file")
        try:
            # Read the source dhcpd.conf configuration file
            bindNamedConFileLocation = str( config.get("base","bindNamedConf"))
            # Open the file
            namedConFile = open(bindNamedConFileLocation,mode='r')
            # Read in the output directory
            dnsmasqConfDir = str(config.get("base","dnsmasqConfigDir"))
            dnsmasqBaseDir = str(config.get("base","dnsmasqBaseDir"))
            dnsmasqDataDir = str(config.get("base","dnsmasqDataDir"))
            dnsmaqConfigDataDir = str(config.get("base","dnsmaqConfigDataDir"))
            # Read in the output file name
            dnsmasqDNSFileName = str(config.get("base","DNSDnsmasqConfFile"))
            dnsmasqHostsFileName= str(config.get("base","DNSDnsmasqHostsFile"))
            dnsmasqHostsFile= os.path.join(dnsmaqConfigDataDir,dnsmasqHostsFileName)
            # Check the path and create it if it doesn't exist
            if not os.path.isdir( dnsmasqConfDir ):
                print "Log directory %s does not exist" % dnsmasqConfDir
                try:
                    os.mkdir( dnsmasqConfDir )
                except:
                    print "Unable to create log directory"
                    return
            # Double check to make sure the directory exists
            if not os.path.isdir( dnsmasqConfDir ):
                print "%s is not a directory" % dnsmasqConfDir
                return
            # Since it must certainly exist now let's make sure it's writable
            if not os.access( dnsmasqConfDir, os.W_OK ):
                print "Directory %s is not writable" % dnsmasqConfDir
                return
            if not os.path.isdir( dnsmaqConfigDataDir ):
                print "Log directory %s does not exist" % dnsmaqConfigDataDir
                try:
                    os.mkdir( dnsmaqConfigDataDir )
                except:
                    print "Unable to create dnsmaq Config Data Dir directory"
                    return
            # Double check to make sure the directory exists
            if not os.path.isdir( dnsmaqConfigDataDir ):
                print "%s is not a directory" % dnsmaqConfigDataDir
                return
            # Since it must certainly exist now let's make sure it's writable
            if not os.access( dnsmaqConfigDataDir, os.W_OK ):
                print "Directory %s is not writable" % dnsmaqConfigDataDir
                return
            # Join the Directory and filename so that we can open the file for writing
            dnsmasqDHCPFile = os.path.join( dnsmasqConfDir , dnsmasqDNSFileName )
            # While we have the file open for writing keep writing to it.  We use the with statement so if the
            # script crashes it will close the file cleanly first flushing the buffers.
            with open(dnsmasqDHCPFile,mode='w') as dnsmasqConf:
                #While we have the file open for reading and keep it open until we are done with it.
                with open(bindNamedConFileLocation,mode='r') as dnsConFile:
                    count = 0
                    DNSDataFiles={}
                    for line in dnsConFile:
                        # Look for zone Entries
                        if line.__contains__("zone") and line.__contains__("{"):
                            splitline = line.split()
                            name = str(splitline[1].strip("\""))
                            count =count + 1
                        if line.__contains__("file") and count > 0:
                            splitline=line.split()
                            filename=splitline[1].strip("\"").strip(";").strip("\"")
                            if len(name) > 2 and not name.__contains__("localhost") and not name.__contains__("in-addr.arpa"):
                                print ("Zone Name: %s \t File Name: %s\n" % (name,filename))
                                DNSDataFiles[name] = filename
                hostsfileName = dnsmasqDataDir + "/" + dnsmasqHostsFileName
                dnsmasqConf.write("addn-hosts=" + hostsfileName)
                with open(dnsmasqHostsFile,mode='w') as dnsmasqHostsConf:
                    for name in DNSDataFiles.keys():
                        splitFileName = DNSDataFiles[name].split('/')
                        DNSDataFiles[name] = os.path.join("../dns_configurations/bind/named",splitFileName[3])
                        print ("%s %s" % (name,DNSDataFiles[name]))
                        with open(DNSDataFiles[name],mode='r') as domainFile:
                            for line in domainFile:
                                if not line.startswith("#"):
                                    InAString = re.compile("IN\sA")
                                    if InAString.search(line):
                                        log2(line)
                                        splitline = line.split()
                                        log2(("Writing %s\t%s to %s\n") % (splitline[3],splitline[0],dnsmasqHostsConf))
                                        dnsmasqHostsConf.write(("%s\t%s\n") % (splitline[3],splitline[0]))
        except:
            handleException("openDhcpdConfFile")
            raise

    processBindNamedconfFile()
