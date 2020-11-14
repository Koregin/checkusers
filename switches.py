#!/usr/bin/env python3
#import pymysql
#import cgi
#import cgitb
import sys
#import codecs
import pexpect
import time
import re
#from ipaddress import ip_address
#import getpass
#sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())



###################################################################################################
#Включение и выключение порта на коммутаторе доступа
#
#Получение параметров с коммутаторов Cisco
def cisco2950(switch_ip, vlan, port, user_id):
    switch_pw = "password"
    switch_en_pw = "enable_password"
    if switch_ip is not None and port is not None:
        child = pexpect.spawn ('telnet '+switch_ip)
        child.expect ('Password: ')
        child.sendline (switch_pw)
        child.expect ('>')
        #Проверка модели коммутатора
        child.sendline ('sh version | i Model number')
        child.expect ('>')
        model1 = child.before.strip()
        model2 = model1.decode('ascii').split('\n')
        for line in model2:
            if re.findall(r'Model number', line):
                model = line[line.find('number')+8:]
#        print (model)
        #Проверка времени работы коммутатора
        child.sendline ('sh version | i uptime')
        child.expect ('>')
        work_time1 = child.before.strip()
        work_time2 = work_time1.decode('ascii').split('\n')
        for line in work_time2:
            if re.findall(r'uptime is', line):
                uptime = line[line.find('is')+3:]
        #Проверка ошибок на порту
        child.sendline ('sh int fa0/%s | i CRC' % port)
        child.expect ('>')
        errors = child.before.strip()
        errors2 = errors.decode('ascii').split('\n')
        errors = errors2[1]
	#Проверка загрузки порта
        child.sendline ('sh int fa0/%s | i rate | e Output' % port)
        child.expect ('>')
        ifload_temp = child.before.strip()
        ifload_temp = ifload_temp.decode('ascii').split('\n')
        ifload_temp = ifload_temp[1:3]
        ifload = []
        for speed in ifload_temp:    #проходим по сырому массиву и сохраняем необходимык данные
            ifload.append(speed[speed.rfind('rate')+5:speed.rfind('bits')-1])  #Выделение bits/sec загрузки input и output и добавление в массив ifload
            ifload.append(speed[speed.rfind(',')+1:speed.rfind('packets')-1])  #Выделение packets загрузки input и output и добавление в массив ifload
        #print(ifload)
        #Проверка IGMP профиля
        child.sendline ('sh ip igmp profile %s | i range' % user_id)
        child.expect ('>')
        igmp1 = child.before.strip()
        igmp2 = igmp1.decode('ascii').split('\n')
        igmp = []
        for line in igmp2:
            if  re.findall(r'range 239.255.1.254 239.255.1.254', line):
                pass
            else:
                igmp.append(line)
        igmp_profile = igmp[1:-1]
#        for i in igmp_profile:
#            print (i)
        #Проверка статуса порта
#        child.sendline ('sh int status | i %s' % vlan)
        child.sendline ('sh int fastEthernet 0/%s status | i Fa0/%s' % (port, port))
        child.expect ('>')
        stat = child.before.strip()
        status = stat.decode('ascii').split('\n')
        #Вывод состояния порта
#        print (status[1])
        int_status = status[1]
        child.sendline ('sh mac address-table int fastEthernet 0/%s' % port)
        child.expect ('>')
        list0 = child.before.strip()
        list1 = list0.decode('ascii').split('\n')
        #Вывод MAC адресов на порту
        macs = []
        for row in list1[6:-2]:
            mac_full = row.split()
#            print (mac_full)
            macs += [mac_full[1]]
#            print (mac_full[1]+"<br>")
#        print (macs)
        #Проверка MVR. К каким группам подключен порт
        child.sendline ('enable')
        child.expect ('Password: ')
        child.sendline (switch_en_pw)
        child.expect ('#')
        child.sendline ('sh mvr int fastEthernet 0/%s members' % port)
        child.expect ('#')
        mvr1 = child.before.strip()
        mvr2 = mvr1.decode('ascii').split('\n')
        arr_channels = mvr2[1:-1]
        channels = []
        try:
            for x in arr_channels:
                ip_ch, dynamic, active = x.split('\t')
                channels.append(ip_ch)
        except ValueError:
            pass
        child.sendline ('sh run int fastEthernet 0/%s' %port)
        child.expect ('#')
        config1 = child.before.strip()
        config2 = config1.decode('ascii').split('\n')
        config = config2[5:-3]
#        config = []
#        for row in arr_config:
#            config.append
#            print (row+"<br>")
        child.sendline('exit')
        return (model, config, uptime, int_status, macs, igmp_profile, channels, errors, ifload)

#Получение параметров с коммутаторов Orion
def orion(switch_ip, vlan, port, user_id):
    model = "Alpha-A28F"
    login = "username"
    switch_pw = "password"
    switch_en_pw = "enable_password"
    if switch_ip is not None and port is not None:
        child = pexpect.spawn ('telnet '+switch_ip)
        child.expect ('Login:')
        child.sendline (login)
        child.expect ('Password:')
        child.sendline (switch_pw)
        i = child.expect (['>', '#'])
        if i == 0:
            child.sendline ('enable')
            child.expect ('Password:')
            child.sendline (switch_en_pw)
            child.expect ('#')
        #Проверка времени работы коммутатора
        child.sendline ('sh version | i uptime')
        child.expect ('#')
        work_time1 = child.before.strip()
        work_time2 = work_time1.decode('ascii').split('\n')
        for line in work_time2:
            if re.findall(r'uptime is', line):
                uptime = line[line.find('is')+3:]
#        print(uptime)
        #Проверка IGMP профиля
        child.sendline ('sh ip igmp profile %s | i range' % user_id)
        child.expect ('#')
        igmp1 = child.before.strip()
        igmp2 = igmp1.decode('ascii').split('\n')
        igmp = []
        for line in igmp2:
            if  re.findall(r'range 239.255.1.254 239.255.1.254', line):
                pass
            else:
                igmp.append(line)
        igmp_profile = igmp[1:-1]
#        print(igmp_profile)
        #Проверка статуса порта
        child.sendline ('sh int port %s | i %s' % (port, port))
        child.expect ('#')
        stat = child.before.strip()
        status = stat.decode('ascii').split('\n')
        #Вывод состояния порта
        int_status = status[1]
#        print (int_status)
        child.sendline ('sh mac-address-table l2-address port %s' % port)
        child.expect ('#')
        list0 = child.before.strip()
        list1 = list0.decode('ascii').split('\n')
        #Вывод MAC адресов на порту
        macs = []
        for row in list1[4:-1]:
            mac_full = row.split()
            macs += [mac_full[0]]
#        print (macs)
        #Проверка MVR. К каким группам подключен порт
        child.sendline ('sh mvr port %s members' % port)
        child.expect ('#')
        mvr1 = child.before.strip()
        mvr2 = mvr1.decode('ascii').split('\n')
        arr_channels = mvr2[1:-1]
        channels = []
        try:
            for x in arr_channels:
                ip_ch, dynamic, active = x.split('\t')
                channels.append(ip_ch)
        except ValueError:
            pass
#        print (channels)
        #Конфигурация порта
        child.sendline ('sh run int port %s' %port)
        child.expect ('#')
        config1 = child.before.strip()
        config2 = config1.decode('ascii').split('\n')
        config = config2[4:-1]
        child.sendline('exit')
        return (model, config, uptime, int_status, macs, igmp_profile, channels)

#Получение параметров с коммутатора Dlink DES-3200-28F
def dlink(switch_ip, vlan, port, user_id):
    model = "Dlink-DES-3200-28F"
    login = "admin"
    switch_pw = "password"
    switch_en_pw = "enable_password"
    if switch_ip is not None and port is not None:
        child = pexpect.spawn ('telnet '+switch_ip)
        child.expect ('UserName:')
        child.sendline (login)
        child.expect ('PassWord:')
        child.sendline (switch_pw)
        i = child.expect (['>', '#'])
        if i == 0:
            child.sendline ('enable')
            child.expect ('Password:')
            child.sendline (switch_en_pw)
            child.expect ('#')
        #Проверка времени работы коммутатора
        child.sendline ('sh time')
        child.expect ('#')
        work_time1 = child.before.strip()
        work_time2 = work_time1.decode('ascii').split('\n')
        for line in work_time2:
            if re.findall(r'Current Time', line):
                uptime = line[line.find(':')+1:]
#        print(uptime)
        #Проверка IGMP профиля
        child.sendline ('sh limited_multicast_addr ports %s' % port)
        child.expect ('#')
        igmp1 = child.before.strip()
        igmp2 = igmp1.decode('ascii').split('\n')
        igmp = []
        for line in igmp2[8:-4]:
            ipgr = line.split()
            if ipgr != []:
              igmp.append(ipgr[2])
        igmp_profile = igmp
#        print(igmp)
        #Проверка статуса порта
        child.sendline ('sh ports %s' % port)
        child.sendline ('q')
        child.expect ('#')
        stat = child.before.strip()
        stat2 = stat.decode('ascii').split('\n')
        #Вывод состояния порта
        int_status = stat2[6].split()
        int_status = int_status[3]
#        print (int_status[3])
        #Вывод MAC адресов на порту
        child.sendline ('sh fdb port %s' % port)
        child.expect ('#')
        child.sendline (' ')
        child.expect ('#')
        list0 = child.before.strip()
        list1 = list0.decode('ascii').split('\n')
        macs = []
        for row in list1[5:-4]:
            mac_full = row.split()
            if mac_full == []:
                pass
            else:
                macs.append(mac_full[2])
#        print (macs)
        channels = []
        #Проверка MVR. К каким группам подключен порт
#        child.sendline ('sh igmp_snooping forwarding vlanid 157')
#        child.expect ('#')
#        child.sendline (' ')
#        child.expect ('#')
#        port = '25'
#        mvr1 = child.before.strip()
#        mvr2 = mvr1.decode('ascii').split('\n\r\n\r')
#        arr1 = []
#        for row in mvr2[3:-2]:
#            arr_mvr = row.split('\n\r')
#            arr_mvr = arr_mvr[2:4]
#            arr1.append(arr_mvr)
#        ###
#        channels = []
#        try:
#            for a in range(len(arr1)):
#                b, ports = arr1[a][1].split(':')
#                c, ip_ch = arr1[a][0].split(':')
#                if re.findall(r""+port+"", ports):
#                    channels.append(ip_ch.replace(' ', ''))
#        except ValueError:
#            pass
#        print (channels)
        child.sendline('logout')
        #Конфигурация порта
        config = "....."
        return (model, config, uptime, int_status, macs, igmp_profile, channels)

#Get parameters from SNR' switches
def snr(switch_ip, vlan, port, user_id):
    login = "admin\r\n"
    switch_pw = "password\r\n"
    switch_en_pw = "enablepassword"
    if switch_ip is not None and port is not None:
        child = pexpect.spawn ('telnet '+switch_ip)
        child.expect ('login:')
        child.sendline (login)
        child.expect (':')
        child.sendline (switch_pw)
        i = child.expect (['>', '#'])
        #print (i)
        if i == 0:
            child.sendline ('enable')
            child.expect ('Password:')
            child.sendline (switch_en_pw)
            child.expect ('#')
        #Проверка модели и времени работы коммутатора
        child.sendline ('sh version')
        child.expect ('#')
        work_time1 = child.before.strip()
        work_time2 = work_time1.decode('ascii').split('\n')
        #print(work_time2)
        i = 0
        for line in work_time2:
            i+=1
            if i == 2:
                model = line.split(',')
                model = model[0].split()
                model = model[0]
        #        print(model)
            if re.findall(r'Uptime', line):
                uptime = line[line.find('is ')+2:].strip()
        #print(uptime)
        #Проверка статуса порта
        child.sendline ('sh int eth stat | i %s' % vlan)
        child.expect ('#')
        stat = child.before.strip()
        stat = stat.decode('ascii').replace('\r\n', ',')
        stat = stat.replace(',,',',')
        stat = stat.split(',')
        stat = stat[1].split()
        int_status = 'Link/Protocol: '+stat[1]+', '+'Speed: '+stat[2]+', '+'Duplex: '+stat[3]
        #print(int_status)
        #Проверка ошибок на порту
        child.sendline ('sh int eth 1/%s | i error' % port)
        child.expect ('#')
        errs = child.before.strip().decode('ascii').split('\n')
        errs = errs[1:-1]
        errors = ''
        for err in errs:
            errors += err.strip().rstrip(',')+', '
        errors = errors.rstrip(', ')
        #print(errors)
        #Port's configuration
        child.sendline ('sh run int eth 1/%s' % port)
        child.expect ('#')
        config = child.before.strip().decode('ascii').split('\n')
        config = config[1:-1]
        #for line in config:
        #    print(line)
        #
        #Вывод MAC адресов на порту
        child.sendline ('sh mac-address-table int eth 1/%s | i DYNAMIC' % port)
        i = child.expect (['#', '--More--'])
        if i == 0:
            pass
        elif i == 1:
        #    print('Too many macs per port')
            child.sendline(' ')
        lines = child.before.strip().decode('ascii').split('\n')
        lines = lines[1:-1]
        macs = []
        for line in lines:
            S = line.split()
            mac = S[1]
            macs.append(mac)
        #print (macs)
        child.sendline('exit')
        return (model, config, uptime, int_status, macs,  errors)

def bdcom(switch_ip, mac_onu):
    login = "service"
    switch_pw = "password"
    switch_en_pw = "enablepassword"
    if switch_ip is not None and mac_onu is not None:
        child = pexpect.spawn ('telnet '+switch_ip)
        child.setwinsize(100,100)
        child.expect ('Username: ')
        child.sendline (login)
        child.expect ('Password: ')
        child.sendline (switch_pw)
        i = child.expect (['>', '#'])
        #print (i)
        if i == 0:
            child.sendline ('enable')
            child.expect ('password:')
            child.sendline (switch_en_pw)
            child.expect ('#')
        child.sendline('sh epon onu-information mac-address ' + mac_onu)
        child.expect ('#')
        onu_inform = child.before.decode('ascii').split('\n')
        onu_inform = onu_inform[6:-3]
        iface = onu_inform[0].split()
        #print(iface)
        onu_power = iface[-1] #ONU power status
        iface = iface[0]
        #sh epon int epon 0/4:2 onu ctc optical-transciever-diagnosis
        if(onu_power == 'power-off'):
            opt_diag = ' ONU не подключена (Последний статус: power-off)'
        elif(onu_power == 'wire-down'):
            opt_diag = ' ONU не подключена (Последний статус: wire-down)'
        else:
            child.sendline('sh epon int '+iface+' onu ctc op')
            child.expect ('#')
            opt_diag = child.before.decode('ascii').split('\n'); opt_diag = opt_diag[-2]
        #Interface config
        child.sendline('sh run int '+iface)
        child.expect ('#')
        config = child.before.decode('ascii').split('\n')
        config = config[5:-1]
        #Version and uptime
        child.sendline('sh version')
        child.expect ('#')
        version = child.before.decode('ascii').split('\n')
        model = version[1]
        uptime = version[-2].split();uptime = uptime[3];uptime = uptime[:-1]
        #Interface status
        child.sendline('sh int '+iface)
        child.expect ('#')
        int_status = child.before.decode('ascii').split('\n'); int_status = int_status[1]
        #MAC addresses on Interface
        child.sendline('sh mac address-table interface '+iface+' | include '+iface)
        child.expect ('#')
        out = child.before.decode('ascii').split('\n'); out = out[6:-1]
        macs = []
        for raw in out:
            mac = raw.split('\t'); mac = mac[1]
            macs.append(mac) 
        child.sendline('exit')
        return (model, config, uptime, int_status, iface, opt_diag, macs)

def zyxel(switch_ip, port):
    login = "admin"
    switch_pw = "password"
    if switch_ip is not None and port is not None:
        child = pexpect.spawn ('telnet '+switch_ip)
        child.setwinsize(100,100)
        child.expect ('User name: ')
        child.sendline (login)
        child.expect ('Password: ')
        child.sendline (switch_pw)
        child.expect ('#')
        #Switch model and uptime
        child.sendline('sh system-information')
        child.expect ('#')
        version = child.before.decode('ascii').split('\n')
        model = version[-2].split(':'); model = 'Zyxel ' + model[1]
        uptime = version[-5].split(' : '); uptime = uptime[0].split('\t:'); uptime = uptime[1][3:13]
        #Port config
        child.sendline('sh int config '+str(port))
        child.expect ('#')
        config = child.before.strip().decode('ascii').split('\n'); config = config[4:-2]
        #Macs per port
        child.sendline('sh mac address-table port '+str(port))
        child.expect ('#')
        macs_l = child.before.strip().decode('ascii').split('\n'); macs_l = macs_l[2:-1]
        macs = []
        for item in macs_l:
            s = item.split()
            macs.append(s[2])
        #Port status
        child.sendline('sh int '+str(port))
        i = child.expect (['#','-- more --'])
        if i == 0:
            pass
        elif i == 1:
            child.sendline(' ')
        port_l = child.before.strip().decode('ascii').split('\n')
        link = port_l[2].replace('\t','').rstrip()
        status = port_l[3].replace('\t','').rstrip()
        int_status = link + status
        #Errors
        errors = port_l[7].replace('\t','').rstrip() + port_l[23].replace('\t','').rstrip()
        child.sendline('exit')
        return (model, config, uptime, int_status, macs, errors)

#CDATA
def cdata(switch_ip, mac_onu, vlan):
    status = 1    # 1 - всё в порядке, 0 - ONU не сконфигурирована правильно
    login = "service\r\n"
    switch_pw = "password\r\n"
    switch_en_pw = "enablepassword"
    if switch_ip is not None and mac_onu is not None:
        child = pexpect.spawn ('telnet '+switch_ip)
        child.setwinsize(100,100)
        child.expect ('Username:')
        child.sendline (login)
        child.expect ('Password:')
        child.sendline (switch_pw)
        i = child.expect (['>', '#'])
        #print (i)
        if i == 0:
            child.sendline ('enable')
            child.expect ('password:')
            child.sendline (switch_en_pw)
            child.expect ('#')
        #Приведение МАК адреса к стандартному для CDATA XX-XX-XX-XX-XX-XX
        mac_onu = mac_onu.replace('.','')
        mac_onu = mac_onu.replace(':','')
        mac_onu = mac_onu.replace('-','')
        temp_mac = ''
        if (len(mac_onu) == 12):
            counter = 1
            for letter in mac_onu:
                temp_mac += letter
                if(counter % 2 == 0) and (counter != 12):
                    temp_mac += '-'
                counter += 1
            mac_onu = temp_mac
        else:
            print("<br><br>В MAC адресе ONU допущена ошибка!!!<br>Дальнейший вывод не возможен.")
            sys.exit(1)
        #Делаем запрос на определение номера ONU по МАК адресу
        child.sendline('sh onu-position ' + mac_onu + '\r\n')
        child.expect ('#')
        onu_inform = child.before.decode('ascii').split('\n')
        #print(onu_inform[1])
        # Вычисляем номер ONU
        iface = onu_inform[1].split(", ")[0][-2:-1]
        # Номер OLT
        olt = onu_inform[1].split(", ")[0][-4:-3]
        # Состояние ONU
        onu_power = onu_inform[1].split(", ")[1].split(":")[1].strip()[:-1] #ONU power status
        #print("Power status: %s" % onu_power)
        if(onu_power == 'offline'):
            opt_diag = ' ONU не подключена'
        elif(onu_power == 'online'):
            #print("ONU включена")
            child.sendline('sh olt %s onu %s ctc optical\r\n' % (olt, iface))
            child.expect ('#')
            opt_diag_list = child.before.decode('ascii').split('\n');
            for row in opt_diag_list:
                if re.search('rx power', row):
                    opt_diag = row.split()[-2]
        else:
            opt_diag = 'Статус неизвестен. Сообщите срочно программисту'
        #Вычсляем номер темплейта на ONU
        child.sendline('sh olt %s all-onu-info\r\n' % olt)
        child.expect ('#')
        onu_inform = child.before.decode('ascii').split('\n')[4:-4]
        ##Поиск ONU с нужным МАК адресом в списке
        curr_Template = ''
        onu_config = []
        for onu in onu_inform:
            if re.findall(mac_onu, onu):
                curr_Template = onu.split()[-1]
                onu_config.append('Template: '+curr_Template)
        ##Проверка текущего шаблона
        if re.findall('system', curr_Template):
            status = 0
            print("Нулевой шаблон. Надо установить 1")
        elif re.findall('1', curr_Template):
            onu_config.append('Шаблон 1')
            #print("Шаблон 1")
        #Проверка VLAN на ONU
        child.sendline('show olt %s onu %s uni 1 ctc vlan-mode\r\n' % (olt, iface))
        child.expect('#')
        onu_vlan = child.before.decode('ascii').split('\n')[1:-1]
        # Проверка вывода VLAN MODE
        if len(onu_vlan) != 4:
            print(onu_vlan[0])
            onu_config.append(onu_vlan[0])
        elif len(onu_vlan) == 4:
            if re.findall('tagged', onu_vlan[0]):
                onu_config.append(onu_vlan[0])    #VLAN MODE
            else:
                status = 0
            if re.findall('0x8100', onu_vlan[1]):
                onu_config.append(onu_vlan[1])    #TPID
            else:
                status = 0
            onu_config.append(onu_vlan[2])        #COS
            onu_config.append(onu_vlan[3])        #VLAN
        #print(opt_diag)
        """
        #Interface config
        child.sendline('sh run int '+iface)
        child.expect ('#')
        config = child.before.decode('ascii').split('\n')
        config = config[5:-1]
        """
        #config = 'конфига пока нет'
        #Version and uptime
        child.sendline('show system uptime\r\n')
        child.expect ('#')
        uptime = child.before.decode('ascii').split('\n')[1].split(':')[1]
        model = 'GR_EP_OLT1-4'
        #Interface status
        int_status = ' '
        #child.sendline('sh int '+iface)
        #child.expect ('#')
        #int_status = child.before.decode('ascii').split('\n'); int_status = int_status[1]
        #MAC addresses on Interface
        child.sendline('sh olt 1 onu %s uni 1 mac-address-table\r\n' % iface)
        child.expect ('#')
        out = child.before.decode('ascii').split('\n')
        #print(out)
        macs = []
        # Prepare regular expression to extract MAC addres in xx:xx:xx:xx:xx:xx format
        p = re.compile(r'(?:[0-9a-fA-F]:?){12}')
        for raw in out:
            #print(raw)
            mac = re.findall(p, raw)
            if mac:
                macs.append(mac[0])
        #print(macs)
        child.sendline('exit')
        return (model, onu_config, uptime, int_status, iface, opt_diag, macs, status)

if __name__ == '__main__':
    print(cdata('10.0.9.226', 'e0-67-b3-c5-0f-4d', '1130'))
#cisco2950('10.0.9.33', '3511', '11', '715')
#cisco2950('10.0.9.42', '2945', '41', '7016')
#No macs
#cisco2950('10.0.9.27', '1487', '22', '43')
#KEV
#cisco2950('10.0.9.118', '3899', '2', '7832')
