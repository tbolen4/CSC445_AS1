import sys, time, datetime, socket
from socket import *

MY_PORT = 2695
BUFSIZE = 4096 
NET_ID = "WOLF>PI"  # change depending on networks used

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
            conn.sendall(data) # echo
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
        j = 0
        for x in range (0, count):
            j = j + 1
            try:
                sock = socket(AF_INET, pack)
                sock.settimeout(3)
                st = datetime.datetime.now()
                sock.connect((server_addr, port))
                st = st.microsecond
                sock.sendall(b_size * 'a')
                data = sock.recv(BUFSIZE)
                rt = datetime.datetime.now()
                rt = rt.microsecond
                sock.close()
                pingTime = rt - st
                if pingTime > 0:
                    pingTime = str(pingTime)
                    dataArray.append(pingTime)
                    print str(j) + ") RTT for " + str(b_size) + " bytes: " + pingTime + " microseconds"
            except timeout:
                print "Socket timed out"
        return dataArray
    if sys.argv[2] == '-u':
        pack = SOCK_DGRAM
        j = 0
        for x in range (0, count):
            j = j + 1
            try:
                sock = socket(AF_INET, pack)
                sock.settimeout(3)
                st = datetime.datetime.now()
                st = st.microsecond
                sock.sendto((b_size * 'a'), (server_addr, port))
                data, addr = sock.recvfrom(BUFSIZE)
                rt = datetime.datetime.now()
                rt = rt.microsecond
                sock.close()
                pingTime = rt - st
                if pingTime > 0:
                    pingTime = str(pingTime)
                    dataArray.append(pingTime)
                    print str(j) + ") RTT for " + str(b_size) + " bytes: " + pingTime + " microseconds"
            except timeout:
                print "Socket timed out"
        return dataArray

def writeToFile(y):
    if sys.argv[2] == '-t':
        p_type = 'TCP'
    else:
        p_type = 'UDP'
    di = "../Data/"
    fileName = di + "Latency_" + NET_ID + "_" + p_type + "_" + str(sys.argv[5]) + ".txt"
    myFile = open(fileName, 'a')
    for x in y:
        myFile.write(x)
        myFile.write(",")
    myFile.close()
    print "Data appended to " + fileName

main()
