import sys, time, datetime, socket
from socket import *

MY_PORT = 2695
BUFSIZE = 16384#4096
NET_ID = "WOLF>PI"  # change depending on networks used and direction

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
        data = recv_basic(conn)
        #data = conn.recv(BUFSIZE)
        print data
        #if not data: break
        conn.sendall(data) # send data back
        #time.sleep(.03)
        print 'Done with', host, 'port', remoteport
        conn.close()

def client():
    port = MY_PORT
    count = eval(sys.argv[2])
    server_addr = sys.argv[3]
    b_size = eval(sys.argv[4])
    dataArray = []
    j = 0
    for x in range (0, count):
        j = j + 1
        try:
            sock = socket(AF_INET, SOCK_STREAM)
            sock.settimeout(5)
            st = datetime.datetime.now()
            sock.connect((server_addr, port))
            st = st.microsecond
            sock.sendall(b_size * 'a')
            #dataBack = recv_basic(sock)
            dataBack = sock.recv(2048)
            print dataBack
            rt = datetime.datetime.now()
            rt = rt.microsecond
            sock.close()
            transferTime = float((rt - st) / 2) # microseconds
            print transferTime
            transferTime = float(transferTime / 1000.0) #milliseconds
            bitCount = float(b_size * 8)
            b_width = float(bitCount / transferTime)
            if b_width > 0:
                dataArray.append(str(b_width))
                print str(j) + ") Throughput: " + str(b_width) + " bits/millisecond"
        except timeout:
            print "Socket timed out"
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

# this needs to be fixed, only finishes when there is socket disconnect
def recv_basic(the_socket):
    total_data=[]
    while True:
        data = the_socket.recv(8192)
        if not data: break
        total_data.append(data)
    return ''.join(total_data)

main()
