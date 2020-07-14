######################################################################################
# LSLGazepoint.py - LSL interface
# Written in 2019 by Gazepoint www.gazept.com
#
# To the extent possible under law, the author(s) have dedicated all copyright 
# and related and neighboring rights to this software to the public domain worldwide. 
# This software is distributed without any warranty.
#
# You should have received a copy of the CC0 Public Domain Dedication along with this 
# software. If not, see <http://creativecommons.org/publicdomain/zero/1.0/>.
######################################################################################

# This Python script uses the Open Gaze API to communicate with the Gazepoint Control 
# application. Eye gaze data is read via the Open Gaze API, and then streamed to LSL.

import socket
import time
import re

import pylsl as lsl

# Commands to send to the Open Gaze API
requests = ['<SET ID="ENABLE_SEND_TIME" STATE="1"/>\r\n',
            '<SET ID="ENABLE_SEND_POG_FIX" STATE="1"/>\r\n',
            '<SET ID="ENABLE_SEND_POG_LEFT" STATE="1"/>\r\n',
            '<SET ID="ENABLE_SEND_POG_RIGHT" STATE="1"/>\r\n',
            '<SET ID="ENABLE_SEND_POG_BEST" STATE="1"/>\r\n',
            '<SET ID="ENABLE_SEND_PUPIL_LEFT" STATE="1"/>\r\n',
            '<SET ID="ENABLE_SEND_PUPIL_RIGHT" STATE="1"/>\r\n',
            '<SET ID="ENABLE_SEND_BLINK" STATE="1"/>\r\n',
            '<SET ID="ENABLE_SEND_PUPILMM" STATE="1"/>\r\n',
            '<SET ID="ENABLE_SEND_DIAL" STATE="1"/>\r\n',
            '<SET ID="ENABLE_SEND_GSR" STATE="1"/>\r\n',
            '<SET ID="ENABLE_SEND_HR" STATE="1"/>\r\n',
            '<SET ID="ENABLE_SEND_HR_PULSE" STATE="1"/>\r\n',
            '<SET ID="ENABLE_SEND_DATA" STATE="1"/>\r\n']

# Socket send
def send(sock,msg):
    msgb = msg.encode()
    print('Sending:', msgb,'\n')
    totalsent = 0
    while totalsent < len(msgb):
        sent = sock.send(msgb[totalsent:])
        if sent == 0:
            raise RuntimeError("socket connection broken")
        totalsent = totalsent + sent
   
# Socket receive   
def receive(sock):
    msg = ''
    numbytes = 0
    t0 = time.time()
    while True:
        chunk = sock.recv(1)
      
        if (len(chunk) == 0):
            break
        msg = msg + (chunk.decode())
        if (msg.endswith('\r\n')):
            #print('Received:',msg.encode())
            break
    
    return msg

if __name__ == "__main__":
    # Connect to Gazepoint Control
    s = socket.socket()
    s.connect(('127.0.0.1',4242))
    
    print('Connected')
    
    # Send request to start streaming data
    numreq = len(requests)
    indreq = 0
    for i in range(numreq):
        send(s,requests[i])
        msg = receive(s)
    
    # Initialize LSL entry
    info = lsl.StreamInfo('Gazepoint','gaze',39,60,'float32','gpuid12345')
    
    # Set meta-data for LSL entry
    info.desc().append_child_value("manufacturer","Gazepoint")
    channels = info.desc().append_child("channels")
    channels.append_child("channel").append_child_value("label","FPOGX") \
                                    .append_child_value("unit","percent") \
                                    .append_child_value("type","gaze")
    channels.append_child("channel").append_child_value("label","FPOGY") \
                                    .append_child_value("unit","percent") \
                                    .append_child_value("type","gaze")
    channels.append_child("channel").append_child_value("label","FPOGS") \
                                    .append_child_value("unit","seconds") \
                                    .append_child_value("type","gaze")
    channels.append_child("channel").append_child_value("label","FPOGD") \
                                    .append_child_value("unit","seconds") \
                                    .append_child_value("type","gaze")
    channels.append_child("channel").append_child_value("label","FPOGID") \
                                    .append_child_value("unit","integer") \
                                    .append_child_value("type","gaze")
    channels.append_child("channel").append_child_value("label","FPOGV") \
                                    .append_child_value("unit","boolean") \
                                    .append_child_value("type","gaze")

    channels.append_child("channel").append_child_value("label","LPOGX") \
                                    .append_child_value("unit","percent") \
                                    .append_child_value("type","gaze")
    channels.append_child("channel").append_child_value("label","LPOGY") \
                                    .append_child_value("unit","percent") \
                                    .append_child_value("type","gaze")
    channels.append_child("channel").append_child_value("label","LPOGV") \
                                    .append_child_value("unit","boolean") \
                                    .append_child_value("type","gaze")
    channels.append_child("channel").append_child_value("label","RPOGX") \
                                    .append_child_value("unit","percent") \
                                    .append_child_value("type","gaze")
    channels.append_child("channel").append_child_value("label","RPOGY") \
                                    .append_child_value("unit","percent") \
                                    .append_child_value("type","gaze")
    channels.append_child("channel").append_child_value("label","RPOGV") \
                                    .append_child_value("unit","boolean") \
                                    .append_child_value("type","gaze")
    channels.append_child("channel").append_child_value("label","BPOGX") \
                                    .append_child_value("unit","percent") \
                                    .append_child_value("type","gaze")
    channels.append_child("channel").append_child_value("label","BPOGY") \
                                    .append_child_value("unit","percent") \
                                    .append_child_value("type","gaze")
    channels.append_child("channel").append_child_value("label","BPOGV") \
                                    .append_child_value("unit","boolean") \
                                    .append_child_value("type","gaze")
    channels.append_child("channel").append_child_value("label","LPCX") \
                                    .append_child_value("unit","percent") \
                                    .append_child_value("type","gaze")   
    channels.append_child("channel").append_child_value("label","LPCY") \
                                    .append_child_value("unit","percent") \
                                    .append_child_value("type","gaze")   
    channels.append_child("channel").append_child_value("label","LPD") \
                                    .append_child_value("unit","float") \
                                    .append_child_value("type","diameter")   
    channels.append_child("channel").append_child_value("label","LPS") \
                                    .append_child_value("unit","unitless") \
                                    .append_child_value("type","gaze")   
    channels.append_child("channel").append_child_value("label","LPV") \
                                    .append_child_value("unit","boolean") \
                                    .append_child_value("type","gaze")
    channels.append_child("channel").append_child_value("label","RPCX") \
                                    .append_child_value("unit","percent") \
                                    .append_child_value("type","gaze")   
    channels.append_child("channel").append_child_value("label","RPCY") \
                                    .append_child_value("unit","percent") \
                                    .append_child_value("type","gaze")  
    channels.append_child("channel").append_child_value("label","RPD") \
                                    .append_child_value("unit","float") \
                                    .append_child_value("type","diameter")  
    channels.append_child("channel").append_child_value("label","RPS") \
                                    .append_child_value("unit","unitless") \
                                    .append_child_value("type","gaze")  
    channels.append_child("channel").append_child_value("label","RPV") \
                                    .append_child_value("unit","boolean") \
                                    .append_child_value("type","gaze")  
    channels.append_child("channel").append_child_value("label","BKID") \
                                    .append_child_value("unit","integer") \
                                    .append_child_value("type","blink")
    channels.append_child("channel").append_child_value("label","BKDUR") \
                                    .append_child_value("unit","seconds") \
                                    .append_child_value("type","blink")  
    channels.append_child("channel").append_child_value("label","BKPMIN") \
                                    .append_child_value("unit","integer") \
                                    .append_child_value("type","blink")  
    channels.append_child("channel").append_child_value("label","LPMM") \
                                    .append_child_value("unit","float") \
                                    .append_child_value("type","diameter")  
    channels.append_child("channel").append_child_value("label","LPMMV") \
                                    .append_child_value("unit","boolean") \
                                    .append_child_value("type","pupil")
    channels.append_child("channel").append_child_value("label","RPMM") \
                                    .append_child_value("unit","float") \
                                    .append_child_value("type","diameter")
    channels.append_child("channel").append_child_value("label","RPMMV") \
                                    .append_child_value("unit","boolean") \
                                    .append_child_value("type","pupil")
    channels.append_child("channel").append_child_value("label","DIAL") \
                                    .append_child_value("unit","float") \
                                    .append_child_value("type","dial")
    channels.append_child("channel").append_child_value("label","DIALV") \
                                    .append_child_value("unit","boolean") \
                                    .append_child_value("type","dial")
    channels.append_child("channel").append_child_value("label","GSR") \
                                    .append_child_value("unit","float") \
                                    .append_child_value("type","gsr")
    channels.append_child("channel").append_child_value("label","GSRV") \
                                    .append_child_value("unit","boolean") \
                                    .append_child_value("type","gsr") 
    channels.append_child("channel").append_child_value("label","HR") \
                                    .append_child_value("unit","float") \
                                    .append_child_value("type","hr") 
    channels.append_child("channel").append_child_value("label","HRV") \
                                    .append_child_value("unit","boolean") \
                                    .append_child_value("type","hr")
    channels.append_child("channel").append_child_value("label","HRP") \
                                    .append_child_value("unit","integer") \
                                    .append_child_value("type","pulse")
    
    
    # Make an LSL outlet
    outlet = lsl.StreamOutlet(info)
    
    # Continuously stream data and push each data sample to the LSL
    while True:
        # Reset data values to 0
        rec_time = 0
        rec_fpogx = 0
        rec_fpogy = 0
        rec_fpogs = 0
        rec_fpogd = 0
        rec_fpogid = 0
        rec_fpogv = 0

        rec_lpogx = 0
        rec_lpogy = 0
        rec_lpogv = 0
        
        rec_rpogx = 0
        rec_rpogy = 0
        rec_rpogv = 0
        
        rec_bpogx = 0
        rec_bpogy = 0
        rec_bpogv = 0
        
        rec_lpcx = 0
        rec_lpcy = 0
        rec_lpd = 0
        rec_lps = 0
        rec_lpv = 0
        
        rec_rpcx = 0
        rec_rpcy = 0
        rec_rpd = 0
        rec_rps = 0
        rec_rpv = 0
        
        rec_bkid = 0
        rec_bkdur = 0
        rec_bkpmin = 0
        
        rec_lpmm = 0
        rec_lpmmv = 0
        
        rec_rpmm = 0
        rec_rpmmv = 0
        
        rec_dial = 0
        rec_dialv = 0
        
        rec_gsr = 0
        rec_gsrv = 0
        
        rec_gsr = 0
        rec_gsrv = 0
        
        rec_hr = 0
        rec_hrv = 0

        rec_hrp = 0
        
        # Read data
        msg = receive(s)
        
        # Data looks like: '<REC TIME="199.98715" FPOGX="0.26676" FPOGY="0.99285" FPOGS="199.84114" FPOGD="0.14601" FPOGID="352" FPOGV="1" />\r\n'
        
        # Parse data string to extract values
        m = re.search('(?<=TIME=")\d*\.\d+|\d+(?=" FPOGX)',msg)
        if (m != None):
            rec_time = float(m.group(0))

        m = re.search('(?<=FPOGX=")\d*\.\d+|\d+(?=" FPOGY)',msg)
        if (m != None):
            rec_fpogx = float(m.group(0))
            
        m = re.search('(?<=FPOGY=")\d*\.\d+|\d+(?=" FPOGS)',msg)
        if (m != None):
            rec_fpogy = float(m.group(0))
            
        m = re.search('(?<=FPOGS=")\d*\.\d+|\d+(?=" FPOGD)',msg)
        if (m != None):
            rec_fpogs = float(m.group(0))
            
        m = re.search('(?<=FPOGD=")\d*\.\d+|\d+(?=" FPOGID)',msg)
        if (m != None):
            rec_fpogd = float(m.group(0))
            
        m = re.search('(?<=FPOGID=")\d*\.\d+|\d+(?=" FPOGV)',msg)
        if (m != None):
            rec_fpogid = float(m.group(0))
            
        m = re.search('(?<=FPOGV=")\d*\.\d+|\d+(?=" LPOGX)',msg)
        if (m != None):
            rec_fpogv = float(m.group(0))  
            
        m = re.search('(?<=LPOGX=")\d*\.\d+|\d+(?=" LPOGY)',msg)
        if (m != None):
            rec_lpogx = float(m.group(0))  
            
        m = re.search('(?<=LPOGY=")\d*\.\d+|\d+(?=" LPOGV)',msg)
        if (m != None):
            rec_lpogy = float(m.group(0))    
            
        m = re.search('(?<=LPOGV=")\d*\.\d+|\d+(?=" RPOGX)',msg)
        if (m != None):
            rec_lpogv = float(m.group(0))  
            
        m = re.search('(?<=RPOGX=")\d*\.\d+|\d+(?=" RPOGY)',msg)
        if (m != None):
            rec_rpogx = float(m.group(0))  
            
        m = re.search('(?<=RPOGY=")\d*\.\d+|\d+(?=" RPOGV)',msg)
        if (m != None):
            rec_rpogy = float(m.group(0))  
            
        m = re.search('(?<=RPOGV=")\d*\.\d+|\d+(?=" BPOGX)',msg)
        if (m != None):
            rec_rpogv = float(m.group(0))  
            
        m = re.search('(?<=BPOGX=")\d*\.\d+|\d+(?=" BPOGY)',msg)
        if (m != None):
            rec_bpogx = float(m.group(0))  
            
        m = re.search('(?<=BPOGY=")\d*\.\d+|\d+(?=" BPOGV)',msg)
        if (m != None):
            rec_bpogy = float(m.group(0))  
            
        m = re.search('(?<=BPOGV=")\d*\.\d+|\d+(?=" LPCX)',msg)
        if (m != None):
            rec_bpogv = float(m.group(0))  
            
        m = re.search('(?<=LPCX=")\d*\.\d+|\d+(?=" LPCY)',msg)
        if (m != None):
            rec_lpcx = float(m.group(0))  
            
        m = re.search('(?<=LPCY=")\d*\.\d+|\d+(?=" LPD)',msg)
        if (m != None):
            rec_lpcy = float(m.group(0))  
            
        m = re.search('(?<=LPD=")\d*\.\d+|\d+(?=" LPS)',msg)
        if (m != None):
            rec_lpd = float(m.group(0)) 
            
        m = re.search('(?<=LPS=")\d*\.\d+|\d+(?=" LPV)',msg)
        if (m != None):
            rec_lps = float(m.group(0)) 
            
        m = re.search('(?<=LPV=")\d*\.\d+|\d+(?=" RPCX)',msg)
        if (m != None):
            rec_lpv = float(m.group(0))  
            
        m = re.search('(?<=RPCX=")\d*\.\d+|\d+(?=" RPCY)',msg)
        if (m != None):
            rec_rpcx = float(m.group(0))  
            
        m = re.search('(?<=RPCY=")\d*\.\d+|\d+(?=" RPD)',msg)
        if (m != None):
            rec_rpcy = float(m.group(0))  
            
        m = re.search('(?<=RPD=")\d*\.\d+|\d+(?=" RPS)',msg)
        if (m != None):
            rec_rpd = float(m.group(0)) 
            
        m = re.search('(?<=RPS=")\d*\.\d+|\d+(?=" RPV)',msg)
        if (m != None):
            rec_rps = float(m.group(0)) 
            
        m = re.search('(?<=RPV=")\d*\.\d+|\d+(?=" BKID)',msg)
        if (m != None):
            rec_rpv = float(m.group(0)) 
            
        m = re.search('(?<=BKID=")\d*\.\d+|\d+(?=" BKDUR)',msg)
        if (m != None):
            rec_bkid = float(m.group(0)) 
            
        m = re.search('(?<=BKDUR=")\d*\.\d+|\d+(?=" BKPMIN)',msg)
        if (m != None):
            rec_bkdur = float(m.group(0))
            
        m = re.search('(?<=BKPMIN=")\d*\.\d+|\d+(?=" LPMM)',msg)
        if (m != None):
            rec_bkpmin = float(m.group(0))
            
        m = re.search('(?<=LPMM=")\d*\.\d+|\d+(?=" LPMMV)',msg)
        if (m != None):
            rec_lpmm = float(m.group(0))
            
        m = re.search('(?<=LPMMV=")\d*\.\d+|\d+(?=" RPMM)',msg)
        if (m != None):
            rec_lpmmv = float(m.group(0))
            
        m = re.search('(?<=RPMM=")\d*\.\d+|\d+(?=" RPMMV)',msg)
        if (m != None):
            rec_rpmm = float(m.group(0))
            
        m = re.search('(?<=RPMMV=")\d*\.\d+|\d+(?=" DIAL)',msg)
        if (m != None):
            rec_rpmmv = float(m.group(0))
            
        m = re.search('(?<=DIAL=")\d*\.\d+|\d+(?=" DIALV)',msg)
        if (m != None):
            rec_dial = float(m.group(0))
            
        m = re.search('(?<=DIALV=")\d*\.\d+|\d+(?=" GSR)',msg)
        if (m != None):
            rec_dialv = float(m.group(0))
            
        m = re.search('(?<=GSR=")\d*\.\d+|\d+(?=" GSRV)',msg)
        if (m != None):
            rec_gsr = float(m.group(0))
            
        m = re.search('(?<=GSRV=")\d*\.\d+|\d+(?=" HR)',msg)
        if (m != None):
            rec_gsrv = float(m.group(0))
            
        m = re.search('(?<=HR=")\d*\.\d+|\d+(?=" HRV)',msg)
        if (m != None):
            rec_hr = float(m.group(0))
            
        m = re.search('(?<=HRV=")\d*\.\d+|\d+(?=" HRP)',msg)
        if (m != None):
            rec_hrv = float(m.group(0))

        m = re.search('(?<=HRP=")\d*\.\d+|\d+(?=" />)',msg)
        if (m != None):
            rec_hrp = float(m.group(0))          
        
        # # Print to consolerec_lpogx = 0
        # print(rec_time, rec_fpogx, rec_fpogy, rec_fpogs, rec_fpogd, rec_fpogid, rec_fpogv, rec_lpogx, rec_lpogy, rec_lpogv, rec_rpogx, rec_rpogy, rec_rpogv, rec_bpogx, rec_bpogy, rec_bpogv,
        # rec_lpcx, rec_lpcy, rec_lpd, rec_lps, rec_lpv, rec_rpcx, rec_rpcy, rec_rpd, rec_rps, rec_rpv, rec_bkid, rec_bkdur, rec_bkpmin, rec_lpmm, rec_lpmmv, rec_rpmm, rec_rpmmv, rec_dial, rec_dialv, rec_gsr, rec_gsrv,
        # rec_hr, rec_hrv, rec_hrp)
        
        # Push data to LSL
        sample = [rec_fpogx, rec_fpogy, rec_fpogs, rec_fpogd, rec_fpogid, rec_fpogv, rec_lpogx, rec_lpogy, rec_lpogv, rec_rpogx, rec_rpogy, rec_rpogv, rec_bpogx, rec_bpogy, rec_bpogv,
        rec_lpcx, rec_lpcy, rec_lpd, rec_lps, rec_lpv, rec_rpcx, rec_rpcy, rec_rpd, rec_rps, rec_rpv, rec_bkid, rec_bkdur, rec_bkpmin, rec_lpmm, rec_lpmmv, rec_rpmm, rec_rpmmv, rec_dial, rec_dialv, rec_gsr, rec_gsrv,
        rec_hr, rec_hrv, rec_hrp]
        outlet.push_sample(sample,rec_time)
        
        
    s.close()
    
    