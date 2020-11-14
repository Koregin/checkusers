#!/usr/bin/env python3
import pymysql
import pexpect
import subprocess
import datetime
import math


#Делаем запрос в БД UTM для получения вланов определенной сети
#db = pymysql.connect(host='192.168.11.4', user='utm5', passwd='utm5', db='UTM5_521007', use_unicode='True', charset='utf8')
#cursor = db.cursor()



def check_speed(ip):
    server_ip = "10.3.0.209"
    port = "22"
    user = "mnemonic"
    user_pw = "ktyjxrfvjz"
    root_pw = "ybrnjrhjvtyfc"
    bgp_pw = "1081978"
    bgp_en_pw = "ybrnjrhjvtyfc"
    try:
        #Login on server
        ch = pexpect.spawn ('ssh -o \"StrictHostKeyChecking no\" %s@%s' % (user, server_ip))
        ch.expect ('password: ')
        ch.sendline (user_pw); ch.expect ('$')
        ch.sendline ('su'); ch.expect ('Password: ')
        ch.sendline (root_pw); ch.expect ('#')
        #Set BGP
        ch.sendline ('cat /proc/net/ipt_ratelimit/download | grep "%s "' % ip); ch.expect('#')
        temp = ch.before.rstrip().decode('utf8').split('\n')
        if len(temp) == 3:
            line = ch.before.rstrip().decode('utf8').split('\n')[1:-1][0]
            downspeed = int(line.split(';')[0].split()[2])/1000000
            down_sec_ago = line.split(';')[1].split()[5]
            if down_sec_ago == 'never':
                pass
            else:
                down_sec_ago = int(down_sec_ago)/1000
        else:
            downspeed, down_sec_ago = 'not_exist', 'not_exist'
        #print('Download speed: ',downspeed, 'Down seconds ago: ',down_sec_ago)
        #
        ch.sendline ('cat /proc/net/ipt_ratelimit/upload | grep "%s "' % ip); ch.expect('#')
        temp = ch.before.rstrip().decode('utf8').split('\n')
        if len(temp) == 3:
            line = ch.before.rstrip().decode('utf8').split('\n')[1:-1][0]
            upspeed = int(line.split(';')[0].split()[2])/1000000
            up_sec_ago = line.split(';')[1].split()[5]
            if up_sec_ago == 'never':
                pass
            else:
                up_sec_ago = int(up_sec_ago)/1000
        else:
            upspeed, up_sec_ago = 'not_exist', 'not_exist'
        #Check IP in ipset
        ch.sendline('ipset --list | grep {}'.format(ip)); ch.expect('#')
        ipset = ch.before.rstrip().decode('utf8').split('\n')[1:-1]
        status = 'off'
        if len(ipset) != 0:
            status = 'on'
        #print('Upload speed: ',upspeed, 'Upload seconds ago: ',up_sec_ago)
        #Logout from server
        ch.sendline ('exit')
        ch.expect ('$')
        ch.sendline ('exit')
        return [downspeed, down_sec_ago, upspeed, up_sec_ago, status]
    except (pexpect.EOF, pexpect.TIMEOUT):
        print(pexpect.TIMEOUT())
        print("Error while trying to do something on Server.")
    else:
        print('Information received!!!')

def nfdump(ip):
    """This function operate nfdump and filter output for single IP"""
    #Find current date and time
    curdata = datetime.datetime.now().strftime("%Y/%m/%d")
    filedata = datetime.datetime.now().strftime("%Y%m%d")
    shifttime = datetime.datetime.now() - datetime.timedelta(minutes=5)
    hour = shifttime.hour
    minute = shifttime.minute

    #Formatting minutes
    rem = math.fmod(minute, 10)
    whole = minute - rem
    if rem <= 5:
        rem = 0
    elif rem > 5:
        rem = 5
    elif rem == 0:
        pass

    minutes = str(int(whole + rem))

    if len(minutes) == 1:
        minutes = '0'+ minutes
    if hour < 10:
        hour = '0'+ str(hour)
    filedata = filedata+str(hour)+minutes
    filtr = "src ip "+ip
    dumpfile = "/nfsen/profiles-data/live/GWShaper/"+curdata+"/nfcapd."+filedata
    nfout = subprocess.check_output(['nfdump', '-r', dumpfile, '-c', '20', filtr])
    nfout = nfout.decode('utf8').split('\n')
    return nfout

def nfdump2(ip):
    """This function operate nfdump and filter output for single IP"""
    #Find current date and time
    curdata = datetime.datetime.now().strftime("%Y/%m/%d")
    datafile = datetime.datetime.now().strftime("%Y%m%d")
    shifttime = datetime.datetime.now() - datetime.timedelta(minutes=5)
    hour = shifttime.hour
    hour2 = shifttime.hour - 1
    minute = shifttime.minute

    #Formatting minutes
    rem = math.fmod(minute, 10)
    whole = minute - rem
    if rem <= 5:
        rem = 0
    elif rem > 5:
        rem = 5
    elif rem == 0:
        pass

    minutes = str(int(whole + rem))
    if len(minutes) == 1:
        minutes = '0'+ minutes
    if hour < 10:
        hour = '0'+str(hour)
    if hour2 < 10:
        hour2 = '0'+str(hour2)
    filedata = datafile+str(hour)+minutes
    filedata2 = datafile+str(hour2)+minutes
    filtr = "src ip "+ip
    filtrd = "dst ip "+ip
    dumpfile = "/nfsen/profiles-data/live/GWShaper/"+curdata+"/nfcapd."+filedata
    rangefile = "/nfsen/profiles-data/live/GWShaper/"+curdata+"/nfcapd."+filedata2+":nfcapd."+filedata
    nfout = subprocess.check_output(['nfdump', '-r', dumpfile, '-c', '20', filtr])
    nfout = nfout.decode('utf8').split('\n')
    downtotal = subprocess.check_output(['nfdump', '-R', rangefile, '-s', 'dstip', filtrd])
    downtotal = downtotal.decode('utf8').split('\n')
    uptotal = subprocess.check_output(['nfdump', '-R', rangefile, '-s', 'srcip', filtr])
    uptotal = uptotal.decode('utf8').split('\n')
    return nfout, downtotal, uptotal

if __name__ == '__main__':
    down,d_sec,up,u_sec, status = check_speed('91.237.209.236')
    print(down,d_sec,up,u_sec, status)
    down,d_sec,up,u_sec, status = check_speed('37.230.148.124')
    print(down,d_sec,up,u_sec, status)
