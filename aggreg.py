#!/usr/bin/env python3
#import pymysql
#import cgi
#import cgitb
#import sys
#import codecs
import pexpect
from ipaddress import ip_address
#import getpass
#sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())


#real_ip = '31.130.126.30'
#vlan = '2416'
#aggregator = None

def check_agg(real_ip):
    #Lenina124's aggregators
    addr_lo16, broadcast_lo16 = map(ip_address, ["37.230.148.1", "37.230.148.255"])
    addr_lo17, broadcast_lo17 = map(ip_address, ["91.237.209.1", "91.237.209.255"])
    addr_lo20, broadcast_lo20 = map(ip_address, ["31.130.120.128", "31.130.120.255"])
    addr_lo21, broadcast_lo21 = map(ip_address, ["95.66.229.1", "95.66.229.255"])
    #Bykova13's aggregators
    addr_lo7, broadcast_lo7 = map(ip_address, ["87.245.199.1", "87.245.199.127"])
    addr_lo8, broadcast_lo8 = map(ip_address, ["31.130.126.1", "31.130.126.255"])
    addr_lo9, broadcast_lo9 = map(ip_address, ["31.130.125.1", "31.130.125.255"])
    addr_lo10, broadcast_lo10 = map(ip_address, ["31.130.124.1", "31.130.124.255"])
    addr_lo11, broadcast_lo11 = map(ip_address, ["31.130.123.1", "31.130.123.255"])
    addr_lo12, broadcast_lo12 = map(ip_address, ["31.130.122.1", "31.130.122.255"])
    addr_lo13, broadcast_lo13 = map(ip_address, ["31.130.121.1", "31.130.121.255"])
    addr_lo14, broadcast_lo14 = map(ip_address, ["31.130.120.1", "31.130.120.127"])
    addr_lo15, broadcast_lo15 = map(ip_address, ["95.66.228.1", "95.66.228.255"])
#
    if real_ip is not None:
        if addr_lo16 <= ip_address(real_ip) <= broadcast_lo16:
            ip = "10.0.100.203"
            hostname = "C4948E_Lenina124"
            loopback = 'loopback16'
            return (ip, hostname, loopback)
        elif addr_lo17 <= ip_address(real_ip) <= broadcast_lo17:
            ip = "10.0.100.203"
            hostname = "C4948E_Lenina124"
            loopback = 'loopback17'
            return (ip, hostname, loopback)
        elif addr_lo20 <= ip_address(real_ip) <= broadcast_lo20:
            ip = "10.0.100.203"
            hostname = "C4948E_Lenina124"
            loopback = 'loopback20'
            return (ip, hostname, loopback)
        elif addr_lo21 <= ip_address(real_ip) <= broadcast_lo21:
            ip = "10.0.100.203"
            hostname = "C4948E_Lenina124"
            loopback = 'loopback21'
            return (ip, hostname, loopback)
        #########################################################
        elif addr_lo7 <= ip_address(real_ip) <= broadcast_lo7:
            ip = "10.0.100.202"
            hostname = "C4948E_Bykova13"
            loopback = 'loopback7'
            return (ip, hostname, loopback)
        elif addr_lo8 <= ip_address(real_ip) <= broadcast_lo8:
            ip = "10.0.100.202"
            hostname = "C4948E_Bykova13"
            loopback = 'loopback8'
            return (ip, hostname, loopback)
        elif addr_lo9 <= ip_address(real_ip) <= broadcast_lo9:
            ip = "10.0.100.202"
            hostname = "C4948E_Bykova13"
            loopback = 'loopback9'
            return (ip, hostname, loopback)
        elif addr_lo10 <= ip_address(real_ip) <= broadcast_lo10:
            ip = "10.0.100.202"
            hostname = "C4948E_Bykova13"
            loopback = 'loopback10'
            return (ip, hostname, loopback)
        elif addr_lo11 <= ip_address(real_ip) <= broadcast_lo11:
            ip = "10.0.100.202"
            hostname = "C4948E_Bykova13"
            loopback = 'loopback11'
            return (ip, hostname, loopback)
        elif addr_lo12 <= ip_address(real_ip) <= broadcast_lo12:
            ip = "10.0.100.202"
            hostname = "C4948E_Bykova13"
            loopback = 'loopback12'
            return (ip, hostname, loopback)
        elif addr_lo13 <= ip_address(real_ip) <= broadcast_lo13:
            ip = "10.0.100.202"
            hostname = "C4948E_Bykova13"
            loopback = 'loopback13'
            return (ip, hostname, loopback)
        elif addr_lo14 <= ip_address(real_ip) <= broadcast_lo14:
            ip = "10.0.100.202"
            hostname = "C4948E_Bykova13"
            loopback = 'loopback14'
            return (ip, hostname, loopback)
        elif addr_lo15 <= ip_address(real_ip) <= broadcast_lo15:
            ip = "10.0.100.202"
            hostname = "C4948E_Bykova13"
            loopback = 'loopback15'
            return (ip, hostname, loopback)
        else:
            print ("Нет такой сети")


def check_agg_local(local_ip):
    #Lenina124's aggregators
    addr_lo5, broadcast_lo5 = map(ip_address, ["172.17.0.1", "172.17.255.255"])
    addr_lo3, broadcast_lo3 = map(ip_address, ["172.22.0.1", "172.22.255.255"])
    addr_lo1, broadcast_lo1 = map(ip_address, ["172.23.0.1", "172.23.255.255"])
    addr_lo2, broadcast_lo2 = map(ip_address, ["172.25.0.1", "172.25.255.255"])
    addr_lo4, broadcast_lo4 = map(ip_address, ["172.32.0.1", "172.32.255.255"])
    addr_lo12, broadcast_lo12 = map(ip_address, ["172.33.0.1", "172.33.255.255"])
    addr_lo13, broadcast_lo13 = map(ip_address, ["172.34.0.1", "172.34.255.255"])
    addr_lo14, broadcast_lo14 = map(ip_address, ["172.35.0.1", "172.35.255.255"])
    #Bykova13's aggregators
    addr_lo18, broadcast_lo18 = map(ip_address, ["172.18.0.1", "172.18.255.255"])
    addr_lo19, broadcast_lo19 = map(ip_address, ["172.19.0.1", "172.19.255.255"])
    addr_lo20, broadcast_lo20 = map(ip_address, ["172.20.0.1", "172.20.255.255"])
    addr_lo21, broadcast_lo21 = map(ip_address, ["172.21.0.1", "172.21.255.255"])
    addr_lo30, broadcast_lo30 = map(ip_address, ["172.30.0.1", "172.30.255.255"])
    addr_lo31, broadcast_lo31 = map(ip_address, ["172.31.0.1", "172.31.255.255"])
#
    if local_ip is not None:
        if addr_lo5 <= ip_address(local_ip) <= broadcast_lo5:
            ip = "10.0.100.203"
            hostname = "C4948E_Lenina124"
            loopback = 'loopback5'
            return (ip, hostname, loopback)
        elif addr_lo3 <= ip_address(local_ip) <= broadcast_lo3:
            ip = "10.0.100.203"
            hostname = "C4948E_Lenina124"
            loopback = 'loopback3'
            return (ip, hostname, loopback)
        elif addr_lo1 <= ip_address(local_ip) <= broadcast_lo1:
            ip = "10.0.100.203"
            hostname = "C4948E_Lenina124"
            loopback = 'loopback1'
            return (ip, hostname, loopback)
        elif addr_lo2 <= ip_address(local_ip) <= broadcast_lo2:
            ip = "10.0.100.203"
            hostname = "C4948E_Lenina124"
            loopback = 'loopback2'
            return (ip, hostname, loopback)
        if addr_lo4 <= ip_address(local_ip) <= broadcast_lo4:
            ip = "10.0.100.203"
            hostname = "C4948E_Lenina124"
            loopback = 'loopback4'
            return (ip, hostname, loopback)
        elif addr_lo12 <= ip_address(local_ip) <= broadcast_lo12:
            ip = "10.0.100.203"
            hostname = "C4948E_Lenina124"
            loopback = 'loopback12'
            return (ip, hostname, loopback)
        elif addr_lo13 <= ip_address(local_ip) <= broadcast_lo13:
            ip = "10.0.100.203"
            hostname = "C4948E_Lenina124"
            loopback = 'loopback13'
            return (ip, hostname, loopback)
        elif addr_lo14 <= ip_address(local_ip) <= broadcast_lo14:
            ip = "10.0.100.203"
            hostname = "C4948E_Lenina124"
            loopback = 'loopback14'
            return (ip, hostname, loopback)
        #########################################################
        elif addr_lo18 <= ip_address(local_ip) <= broadcast_lo18:
            ip = "10.0.100.202"
            hostname = "C4948E_Bykova13"
            loopback = 'loopback16'
            return (ip, hostname, loopback)
        elif addr_lo19 <= ip_address(local_ip) <= broadcast_lo19:
            ip = "10.0.100.202"
            hostname = "C4948E_Bykova13"
            loopback = 'loopback2'
            return (ip, hostname, loopback)
        elif addr_lo20 <= ip_address(local_ip) <= broadcast_lo20:
            ip = "10.0.100.202"
            hostname = "C4948E_Bykova13"
            loopback = 'loopback3'
            return (ip, hostname, loopback)
        elif addr_lo21 <= ip_address(local_ip) <= broadcast_lo21:
            ip = "10.0.100.202"
            hostname = "C4948E_Bykova13"
            loopback = 'loopback6'
            return (ip, hostname, loopback)
        elif addr_lo30 <= ip_address(local_ip) <= broadcast_lo30:
            ip = "10.0.100.202"
            hostname = "C4948E_Bykova13"
            loopback = 'loopback4'
            return (ip, hostname, loopback)
        elif addr_lo31 <= ip_address(local_ip) <= broadcast_lo31:
            ip = "10.0.100.202"
            hostname = "C6509_Bykova13"
            loopback = 'loopback5'
            return (ip, hostname, loopback)
        else:
            print ("Нет такой сети")




#aggreg = checkaggreg('31.130.120.129')
#print (aggreg[0]+"Hostname: "+aggreg[1])