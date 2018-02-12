
import sys, time, datetime, socket
from socket import *

MY_PORT = 2695
BUFSIZE = 1024 # max amount of data recieved at once, change if sending more???
NET_ID = "testNetwork"  # change depending on networks used

# do timestamp on both server and client for throughput or divide rtt by 2?
# see if a char is 1 byte in python 2
# test UDP parts see if I run into errors, may need to download more libraries
# whats wrong with UDP and python
# put computer on same ntp server as Linux server, get timestamp from client and server for throughput
# see if method calls use same ntp server as cpu

def main():
    if len(sys.argv) < 3:
        usage()
    if sys.argv[1] == '-s':
        server()
    elif sys.argv[1] == '-c':
        if len(sys.argv) >= 6:
            dataPing = client()
            if len(sys.argv) == 7:
                if sys.argv[6] == '-f':
                    writeToFile(dataPing)
                else:
                    usage()
    else:
        usage()

def usage():
    sys.stdout = sys.stderr #learn this
    print 'Usage'
    print "Server: latency.py -s -t/-u (TCP/UDP)"
    print "Client: latency.py -c -t/-u (TCP/UDP) pingCount serverIP byteAmount -f (write to file)"
    sys.exit(2) # end program with command line syntax error

def server():
    port = MY_PORT
    if sys.argv[2] == '-t':
        pack = SOCK_STREAM
    if sys.argv[2] == '-u':
        pack = SOCK_DGRAM
    else:
        pack = SOCK_STREAM
    s = socket(AF_INET, pack)
    s.bind(('', port)) # bind to any incoming address
    if sys.argv[2] == '-t':
        s.listen(5) # queue 5 connections, only tcp
    print 'Server listening...'
    if sys.argv[2] == '-t':     # for tcp only
        while 1:
            conn, (host, remoteport) = s.accept()
            data = conn.recv(BUFSIZE)
            if not data: break
            conn.send(data) # echo
            print 'Done with', host, 'port', remoteport
            conn.close()
    elif sys.argv[2] == '-u':   # for udp only
        while 1:
            data, addr = s.recvfrom(BUFSIZE)
            if not data: break
            print "Recieved Data: " + data
            s.sendto(data, (addr)) # echo

def client():
    port = MY_PORT
    count = eval(sys.argv[3])
    server_addr = sys.argv[4]
    b_size = eval(sys.argv[5])
    dataArray = []
    if sys.argv[2] == '-t':
        pack = SOCK_STREAM
        for x in range (0, count):
            sock = socket(AF_INET, pack)
            sock.connect((server_addr, port))
            st = datetime.datetime.now()
            st = st.microsecond
            sock.send(b_size * 'a')
            data = sock.recv(BUFSIZE)
            rt = datetime.datetime.now()
            rt = rt.microsecond
            sock.close()
            pingTime = str(rt - st)
            dataArray.append(pingTime)
            print "RTT for " + str(b_size) + " bytes: " + pingTime + " microseconds"
        return dataArray
    if sys.argv[2] == '-u':
        pack = SOCK_DGRAM
        for x in range (0, count):
            sock = socket(AF_INET, pack)
            st = datetime.datetime.now()
            st = st.microsecond
            sock.sendto((b_size * 'a'), (server_addr, port))
            data, addr = sock.recvfrom(BUFSIZE) # why dont I need to bind to address first if UDP is connectionless
            rt = datetime.datetime.now()
            rt = rt.microsecond
            sock.close()
            pingTime = str(rt - st)
            dataArray.append(pingTime)
            print "RTT for " + str(b_size) + " bytes: " + pingTime + " microseconds"
        return dataArray

def writeToFile(y):
    if sys.argv[2] == '-t':
        p_type = 'TCP'
    else:
        p_type = 'UDP'
    fileName = "Latency_" + NET_ID + "_" + p_type + "_" + str(sys.argv[5]) + ".txt"
    myFile = open(fileName, 'a')
    for x in y:
        myFile.write(x)
        myFile.write(",")
    myFile.close()
    print "Data appended to " + fileName

main()
