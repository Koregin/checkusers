#!/usr/bin/env python3
import pexpect
import re

def change_loopback(aggregator, vlan, loopback):
    print(aggregator, vlan, loopback)
    """Change loopback for interface Vlan on aggregate cisco
    """
    switch_ip = aggregator
    port = "22"
    user = "service"
    switch_pw = "1081978"
    switch_en_pw = "ybrnjrhjvtyfc"
    #
    child = pexpect.spawn ('telnet '+switch_ip)
    child.expect ('Username: ')
    child.sendline (user); child.expect ('Password: ')
    child.sendline (switch_pw); child.expect ('>')
    child.sendline ('enable'); child.expect ('Password')
    child.sendline (switch_en_pw); child.expect ('#')
    child.sendline ('conf t'); child.expect ('\(config\)#')
    #Change loopback on Cisco
    child.sendline ('int vlan'+str(vlan))
    child.expect ('\(config-if\)#')
    child.sendline ('ip unnumbered '+loopback)
    child.expect ('\(config-if\)#')
    child.sendline ('exit'); child.expect ('\(config\)#')
    child.sendline ('end'); child.expect ('#')
    child.sendline ('quit')

def create_policy(aggregator, vlan, policy):
    """Change loopback for interface Vlan on aggregate cisco
    """
    switch_ip = aggregator
    port = "22"
    user = "service"
    switch_pw = "1081978"
    switch_en_pw = "ybrnjrhjvtyfc"
    #
    child = pexpect.spawn ('telnet '+switch_ip)
    child.expect ('Username: ')
    child.sendline (user); child.expect ('Password: ')
    child.sendline (switch_pw); child.expect ('>')
    child.sendline ('enable'); child.expect ('Password')
    child.sendline (switch_en_pw); child.expect ('#')
    child.sendline ('conf t'); child.expect ('\(config\)#')
    #Change loopback on Cisco
    child.sendline ('int vlan'+str(vlan))
    child.expect ('\(config-if\)#')
    child.sendline (policy)
    child.expect ('\(config-if\)#')
    child.sendline ('exit'); child.expect ('\(config\)#')
    child.sendline ('end'); child.expect ('#')
    child.sendline ('quit')

def change_helper(aggregator, vlan, helper, new_helper):
    """Change helper-address for interface Vlan on aggregate cisco
    """
    switch_ip = aggregator
    port = "22"
    user = "service"
    switch_pw = "1081978"
    switch_en_pw = "ybrnjrhjvtyfc"
    #
    child = pexpect.spawn ('telnet '+switch_ip)
    child.expect ('Username: ')
    child.sendline (user); child.expect ('Password: ')
    child.sendline (switch_pw); child.expect ('>')
    child.sendline ('enable'); child.expect ('Password')
    child.sendline (switch_en_pw); child.expect ('#')
    child.sendline ('conf t'); child.expect ('\(config\)#')
    #Change loopback on Cisco
    child.sendline ('int vlan'+str(vlan))
    child.expect ('\(config-if\)#')
    child.sendline ('no ip helper-address '+helper)
    child.expect ('\(config-if\)#')
    child.sendline ('ip helper-address '+new_helper)
    child.expect ('\(config-if\)#')
    child.sendline ('exit'); child.expect ('\(config\)#')
    child.sendline ('end'); child.expect ('#')
    child.sendline ('quit')

def create_int(aggregator, vlan, loopback, helper_address, policy):
    """Create interface on aggregate cisco
    """
    print(aggregator, vlan, loopback, helper_address, policy)
    switch_ip = aggregator
    port = "22"
    user = "service"
    switch_pw = "1081978"
    switch_en_pw = "ybrnjrhjvtyfc"
    #
    child = pexpect.spawn ('telnet '+switch_ip)
    child.expect ('Username: ')
    child.sendline (user); child.expect ('Password: ')
    child.sendline (switch_pw); child.expect ('>')
    child.sendline ('enable'); child.expect ('Password')
    child.sendline (switch_en_pw); child.expect ('#')
    child.sendline ('conf t'); child.expect ('\(config\)#')
    child.sendline ('ip dhcp snooping vlan '+str(vlan)); child.expect ('\(config\)#')
    #Create interface on Cisco
    child.sendline ('int vlan'+str(vlan))
    child.expect ('\(config-if\)#')
    child.sendline ('ip unnumbered '+loopback); child.expect ('\(config-if\)#')
    child.sendline ('ip helper-address '+helper_address); child.expect ('\(config-if\)#')
    child.sendline (policy); child.expect ('\(config-if\)#')
    child.sendline ('no ip redirects'); child.expect ('\(config-if\)#')
    child.sendline ('no ip unreachables'); child.expect ('\(config-if\)#')
    child.sendline ('no ip proxy-arp'); child.expect ('\(config-if\)#')
    child.sendline ('no shutdown'); child.expect ('\(config-if\)#')
    child.sendline ('exit'); child.expect ('\(config\)#')
    child.sendline ('end'); child.expect ('#')
    child.sendline ('quit')

def clear_counters(switch, swport):
    """Clear errors counters on port
    """
    switch_ip = switch
    switch_pw = "1081978"
    switch_en_pw = "1081978kevltd"
    ###
    child = pexpect.spawn ('telnet '+switch_ip)
    child.expect ('Password: ')
    child.sendline (switch_pw); child.expect ('>')
    child.sendline ('enable'); child.expect ('Password: ')
    child.sendline (switch_en_pw); child.expect ('#')
    #Clear counters
    child.sendline ('clear counters fa0/'+swport); child.expect ('[confirm]')
    child.sendline (''); child.expect('#')
    child.sendline ('quit')

def offonport(switch, swport):
    """Disable|Enable port
    """
    switch_ip = switch
    switch_pw = "1081978"
    switch_en_pw = "1081978kevltd"
    ###
    child = pexpect.spawn ('telnet '+switch_ip)
    child.expect ('Password: ')
    child.sendline (switch_pw); child.expect ('>')
    child.sendline ('enable'); child.expect ('Password: ')
    child.sendline (switch_en_pw); child.expect ('#')
    #
    child.sendline ('conf t'); child.expect ('\(config\)#')
    child.sendline ('int fa0/'+swport)
    child.expect ('\(config-if\)#')
    child.sendline ('shutdown'); child.expect ('\(config-if\)#')
    child.sendline ('no shutdown'); child.expect ('\(config-if\)#')
    child.sendline ('exit'); child.expect ('\(config\)#')
    child.sendline ('end'); child.expect ('#')
    child.sendline ('quit')

def cdata_apply_onu(switch_ip, mac_onu, vlan):
    login = "service\r\n"
    switch_pw = "1081978\r\n"
    switch_en_pw = "ybrnjrhjvtyfc"
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
        idOnu = onu_inform[1].split(", ")[0][-2:-1]
        olt = onu_inform[1].split(", ")[0][-4:-3]
        print("OLT: %s, idOnu: %s" % (olt, idOnu))
        #Вычсляем номер темплейта на ONU
        child.sendline('sh olt %s all-onu-info\r\n' % olt)
        child.expect ('#')
        onu_inform = child.before.decode('ascii').split('\n')[4:-4]
        # Поиск ONU с нужным МАК адресом в списке
        curr_Template = ''
        for onu in onu_inform:
            if re.findall(mac_onu, onu):
                curr_Template = onu.split()[-1]
                print('Template: '+curr_Template)
        # Назначение шаблона на ONU
        child.sendline('system onu-template-config-user 1\r\n')
        child.expect('#')
        child.sendline('apply %s %s\r\n' % (olt, idOnu))
        child.expect('#')
        child.sendline('exit\r\n')
        # Назначить нужный VLAN на ONU
        child.sendline('olt %s\r\n' % olt)
        child.expect('#')
        child.sendline('onu %s\r\n' % idOnu)
        child.expect('#')
        child.sendline('uni 1\r\n')
        child.expect('#')
        child.sendline('ctc vlan-mode tag 0x8100 0 %s\r\n' % vlan)
        child.expect('#')
        child.sendline('exit\r\n')
        child.expect('#')
        child.sendline('exit\r\n')
        child.expect('#')
        child.sendline('exit\r\n')
        child.expect('#')
        """
        #Проверка текущего шаблона
        if re.findall('system', curr_Template):
            print("Нулевой шаблон. Надо установить 1")
        elif re.findall('1', curr_Template):
            print("Шаблон 1")
        #Проверка VLAN на ONU
        child.sendline('show olt %s onu %s uni 1 ctc vlan-mode\r\n' % (olt, idOnu))
        child.expect('#')
        onu_vlan = child.before.decode('ascii').split('\n')[1:-1]
        # Проверка вывода VLAN MODE
        if len(onu_vlan) != 4:
            print(onu_vlan[0])
        elif len(onu_vlan) == 4:
            if re.findall('tagged', onu_vlan[0]):
                print("VLAN MODE: Tagged")
            if re.findall('0x8100', onu_vlan[1]):
                print('TPID: 0x8100')
        """
        #print(onu_vlan)


if __name__ == '__main__':
    cdata_apply_onu('10.0.9.226', 'e0-67-b3-e6-b6-24', '1130')
    cdata_apply_onu('10.0.9.226', 'e0-67-b3-c4-55-28', '1132')
    