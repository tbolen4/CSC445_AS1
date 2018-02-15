import sys, time, datetime, socket
from socket import *

MY_PORT = 2695
BUFSIZE = 1024 # max amount of data recieved at once, change if sending more???
NET_ID = "testNetwork_dir"  # change depending on networks used and direction


def main():
    if len(sys.argv) < 2:
        usage()
    if sys.argv[1] == '-s':
        server()
    elif sys.argv[1] == '-c':
        if len(sys.argv) >= 5:
            dataPing = client()
            if len(sys.argv) == 6:
                if sys.argv[5] == '-f':
                    writeToFile(dataPing)
                else:
                    usage()
    else:
        usage()

def usage():
    sys.stdout = sys.stderr # learn this
    print 'Usage'
    print "Server: throughput.py -s"
    print "Client: throughput.py -c pingCount serverIP byteAmount -f (write to file)"
    sys.exit(2) # end program with command line syntax error

def server():
    port = MY_PORT
    s = socket(AF_INET, SOCK_STREAM)
    s.bind(('', port)) # bind to any incoming address
    s.listen(5) # queue 5 connections
    print 'Server listening...'
    while 1:
        conn, (host, remoteport) = s.accept()
        data = conn.recv(BUFSIZE)
        if not data: break
        conn.send(data) # send timestamp back
        print 'Done with', host, 'port', remoteport
        conn.close()

def client():
    port = MY_PORT
    count = eval(sys.argv[2])
    server_addr = sys.argv[3]
    b_size = eval(sys.argv[4])
    dataArray = []
    for x in range (0, count):
        sock = socket(AF_INET, SOCK_STREAM)
        sock.connect((server_addr, port))
        st = datetime.datetime.now()
        st = st.microsecond
        sock.send(b_size * 'a')
        dataBack = sock.recv(BUFSIZE)
        rt = datetime.datetime.now()
        rt = rt.microsecond
        sock.close()
        transferTime = float((rt - st) / 2)
        bitCount = float(b_size * 8)
        b_width = bitCount / transferTime
        b_width = float(b_width * 1000)
        if b_width > 0:
            dataArray.append(str(b_width))
        print "Throughput: " + str(b_width) + " bits/second"
    return dataArray

def writeToFile(y):
    di = "../Data/"
    fileName = di + "Throughput_" + NET_ID + "_" + str(sys.argv[4]) + ".txt"
    myFile = open(fileName, 'a')
    for x in y:
        myFile.write(x)
        myFile.write(",")
    myFile.close()
    print "Data appended to " + fileName

main()
