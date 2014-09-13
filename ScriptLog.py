import os
import time
import sys
import traceback
"""
ScriptLog.py - A scripting library that allows for out put to the screen, a file or both.  You can use different parts of this package
    to tag what you are doing at the time of the logging.  It takes logging one step farther by also showing the trace back information.  
    Logger - Does the main work but is not called directly.
        append, adds to the end of the log
        __checkStream - Check to see if the stream and log file is already initialized
        end - Closes the stream and file
        __init__ - does nothing
        openLog - opens or creates the path and log file.
    handleException - 
    
"""

lineSeparator = os.linesep
fileSeparator = os.pathsep
stars = "*" * 60

class Logger:
    __stream = None
    __isOpen = 0
    __isSystemStream = 0
    def append( self, s ):
        if self.__checkStream():
            self.__stream.write( s )

    def __checkStream( self ):
        if self.__stream == None:
            print "Log file has NOT been explicitly initialized, creating default log file"
            self.openLog( ".", "script.log" )
        return ( not self.__stream == None )

    def end( self ):
        if self.__checkStream():
            try:
                self.__stream.flush()
                if not self.__isSystemStream:
                    self.__stream.close()
                self.__stream = None
            except:
                pass

    def __init__ ( self ):
        pass

    def openLog( self, logdir, logfilename, logtruncate = 1 ):
        if self.__stream == None:
            if logtruncate:
                mode = "w"
            else:
                mode = "a+"
            if logfilename == None and logdir == None:
                self.__stream = sys.stdout
                self.__isOpen = 1
                self.__isSystemStream = 1
            else:
                if not os.path.isdir( logdir ):
                    print "Log directory %s does not exist" % logdir
                    try:
                        os.mkdir( logdir )
                    except:
                        print "Unable to create log directory"
                    return
                if not os.path.isdir( logdir ):
                    print "%s is not a directory" % logdir
                    return
                if not os.access( logdir, os.W_OK ):
                    print "Directory %s is not writable" % logdir
                    return
                fullfilename = os.path.join( logdir , logfilename )
                print( "Detailed log will be written to file %s" % fullfilename )
                try:
                    self.__stream = open( fullfilename, mode, 0 )
                    self.__isOpen = 1
                except:
                    print( "Cannot open log file %s, logging will be disabled" % fullfilename )
        else:
            print ( "Log file already open" )

""" End of the Logger Class"""

def handleException( method ):
    #
    # Handles an exception:
    # Prints exception message, closes log and exits 
    #
    msg = "An exception has occurred in %s.\n \
        Exception type: %s \n \
        Exception value: %s \n \
        The filename, line number, function, statement and value of the exception are: \n \
        %s \n \
        Please make any necessary corrections and try again.\n" % ( method, sys.exc_info()[0], sys.exc_info()[1], traceback.extract_tb( sys.exc_info()[2] ) )
    log2( msg )


def __get_current_traceback():
    try:
        raise ZeroDivisionError
    except ZeroDivisionError:
        f = sys.exc_info()[2].tb_frame.f_back
    list = []
    limit = 10
    n = 0
    while f is not None and ( limit is None or n < limit ):
        lineno = f.f_lineno
        co = f.f_code
        filename = co.co_filename
        # strip off .py extension
        st_fname = filename.replace( ".py", "" )
        ind = st_fname.rfind( "\\" )
        if ind != -1:
            fname = st_fname[ind + 1:]
        else:
            fname = st_fname.split( "/" )[-1]

        name = co.co_name
        list.append( ( fname, lineno, name ) )
        f = f.f_back
        n = n + 1
    return list


def entry ( message = "" ):
    log ( message, ">" )
def info ( message = "" ):
    log ( message, "I" )
def error( message ):
    log ( message, "E" )
def warning( message ):
    log ( message, "W" )
def exit ( message = "" ):
    log ( message, "<" )
def debug ( message ):
    log ( message, "D" )

def banner( msg ):
    log ( stars )
    log ( "*" )
    log ( msg )
    log ( "*" )
    log ( stars )

# Flushes and closes log file.
def closeLog():
    banner ( "Log file closed" )
    logger.end()

def close():
    closeLog()
#**********************************************************************
# Logging routines.
# Use log instead of puts to log a message.
# For important message use log2, it logs a message into a file + show on screen
#**********************************************************************
# Message will be logged to logfile
# Use log2 to copy to stdout
def log ( message = "", level = "I", addeol = 1 ):
    line = 0
    modul = ""
    func = ""
    stack = __get_current_traceback()
    for fr in stack:
        modul = fr[0]
        if modul != __name__:
            line = fr[1]
            func = fr[2]
            break
    try:
        if modul == "<string>":
            modul = "<main_script>"
        elif not modul.endswith( "py" ):
            modul += ".py"
        formatted_msg = "%s |%s| %s (%s:%d) %s" % ( time.ctime( time.time() ), level, func, modul, line, message )
        logger.append( formatted_msg )
        if ( addeol ):
            logger.append( lineSeparator )
    except:
    # we want to ignore logging errors
        print ( message )
        raise

# Logs message to logfile AND stdout
def log2 ( message ):
    print( message )
    log ( message )

def lopen( fullFileName, dir = "/var/log/" ):
    if ( fullFileName == "stdout" ):
        logger.openLog ( None, None, 0 )
    else:
        print "opening log file: %s/%s" % ( dir, fullFileName )
        logger.openLog ( dir, fullFileName, 0 )
        banner ( "Log file open " )

logger = Logger()
