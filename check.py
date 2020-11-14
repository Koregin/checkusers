#!/usr/bin/env python3
#data changing is 10.12.2018 17:06
import pymysql
import cgi
import sys
import codecs
import pexpect
import re
import time
import aggreg
import switches
import csv
import tokenize
import base64
import checkfunc
from netaddr import IPNetwork, IPAddress
import services

t1 = time.time()
opt_diag = None
onu_status = None
sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

script_name = 'check.py'
ifload = []   # Переменная массива загрузки порта

def checkpolicy(ip):
    print(ip)
    junroutes = '/var/www/check/cgi-bin/scripts/shaper_routes.txt'
    output = open(junroutes)
    policy = 'no ip policy INET_CHANNEL2'
    for route in output:
        net, gw = route.split()[2], route.split()[3]
        #gw = gw[:-1]
        #Check ip enter to network
        if IPAddress(ip) in IPNetwork(net):
            if gw == '192.168.16.5': #Gateway Cisco 4948 Bykova13
                policy = 'ip policy route-map INET_CHANNEL2'
                break
            elif gw == '192.168.16.4': #Gateway Cisco 4948 Bykova13
                policy = 'ip policy route-map Mikrotik_Main'
                break
            else:
                policy = ''
                break
        else:
            policy = 'ip policy route-map INET_BGP2'
    return policy

print ("Content-type:text/html;charset=utf-8")
print ()
print ("<html>")
print ("<head>")
print ("<meta charset=\"utf-8\" />")
print ("</head>")
a = """<body>
<script>
var show;
function hidetxt(type){
 param=document.getElementById(type);
 if(param.style.display == "none") {
 if(show) show.style.display = "none";
 param.style.display = "block";
 show = param;
 }else param.style.display = "none"
}
</script>
"""
print(a)
#print ("<img src=\"http://check.office.net/cgi-bin/check/checkusers3.jpg\">")
data_uri = base64.b64encode(open('checkusers3.jpg', 'rb').read()).decode('utf-8').replace('\n', '')
img_tag = '<img src="data:image/jpg;base64,{0}">'.format(data_uri)
print(img_tag)

def forma(action, floopback, fhelper_address, fcurrent_helper_address, policy, sw_ip='', port_number='', vlan='', mac_onu=''):
    print('<form method=POST action="'+script_name+'?id='+user_id+'">')
    if action == 'clear_counters':
        print('<input type="text" name="action" value="'+action+'" hidden />')
        print('<input type="text" name="sw_ip" value="'+sw_ip+'" hidden />')
        print('<input type="text" name="port_number" value="'+str(port_number)+'" hidden />')
        print('<input type="submit" value="Обнулить ошибки">')
    elif action == 'offonport':
        print('<input type="text" name="action" value="'+action+'" hidden />')
        print('<input type="text" name="sw_ip" value="'+sw_ip+'" hidden />')
        print('<input type="text" name="port_number" value="'+str(port_number)+'" hidden />')
        print('<input type="submit" value="Выключить/Включить порт">')
    elif action == 'cdata_apply_onu':
        print('<input type="text" name="action" value="'+action+'" hidden />')
        print('<input type="text" name="sw_ip" value="'+sw_ip+'" hidden />')
        print('<input type="text" name="vlan" value="'+vlan+'" hidden />')
        print('<input type="text" name="mac_onu" value="'+str(mac_onu)+'" hidden />')
        print('<input type="submit" value="Настроить ONU">')
    else:
        print('<input type="text" name="aggregator" value="'+aggregator+'" hidden />')
        print('<input type="text" name="vlan" value="'+vlan+'" hidden />')
        #
        if floopback != 'fake':
            print('<input type="text" name="loopback" value="'+floopback+'" hidden />')
        if fhelper_address != 'fake':
            print('<input type="text" name="helper_address" value="'+fhelper_address+'" hidden />')
            if fcurrent_helper_address != 'fake':
                print('<input type="text" name="current_helper_address" value="'+fcurrent_helper_address+'" hidden />')
        print('<input type="text" name="policy" value="'+policy+'" hidden />')
        print('<input type="text" name="action" value="'+action+'" hidden />')
        print('<input type="submit" value="Исправить">')
    print('</form>')

form = cgi.FieldStorage()
#ip = form.getvalue('real_ip')
user_id = form.getvalue('id')

#Data for change vlan interface
cur_aggregator = form['aggregator'].value if 'aggregator' in form else None
cur_vlan = form['vlan'].value if 'vlan' in form else None
#print("Cur vlan = %s" % cur_vlan)
cur_loopback = form['loopback'].value if 'loopback' in form else None
cur_helper_address = form['helper_address'].value if 'helper_address' in form else None
cur_helper_address_old = form['current_helper_address'].value if 'current_helper_address' in form else None
cur_policy = form['policy'].value if 'policy' in form else 'no policy'
cur_action = form['action'].value if 'action' in form else None
sw_ip = form['sw_ip'].value if 'sw_ip' in form else None
port = form['port_number'].value if 'port_number' in form else None
mac_onu = form['mac_onu'].value if 'mac_onu' in form else None
#vlan = form['vlan'].value if 'vlan' in form else None


#Check data from form. If data exist accomplish function change_loopback
if cur_action == None:
    pass
else:
    if cur_action == 'change_loopback':
        checkfunc.change_loopback(cur_aggregator, cur_vlan, cur_loopback)
    elif cur_action == 'create_int':
        checkfunc.create_int(cur_aggregator, cur_vlan, cur_loopback, cur_helper_address, cur_policy)
    elif cur_action == 'change_helper':
        checkfunc.change_helper(cur_aggregator, cur_vlan, cur_helper_address_old, cur_helper_address)
    elif cur_action == 'create_policy':
        #checkfunc.create_policy(cur_aggregator, cur_vlan, cur_loopback, cur_helper_address, cur_policy)
        checkfunc.create_policy(cur_aggregator, cur_vlan, cur_policy)
    elif cur_action == 'clear_counters':
        #print(sw_ip, port)
        checkfunc.clear_counters(sw_ip, port)
    elif cur_action == 'offonport':
        #print(sw_ip, port)
        checkfunc.offonport(sw_ip, port)
    elif cur_action == 'cdata_apply_onu':
        checkfunc.cdata_apply_onu(sw_ip, mac_onu, cur_vlan)

#user_id = '1861'
errors = 'No'

#DB Abonents connect and select
db = pymysql.connect(host='10.3.0.36', user='dbusers', passwd='dbusers', db='abonents', use_unicode='True', charset='utf8')
cursor = db.cursor()
query = 'select full_name as username, flat, port_number, vlan, INET_NTOA(u.ip) as local_ip, \
                    INET_NTOA(u.ip2) as local_ip2, INET_NTOA(u.ip3) as local_ip3, INET_NTOA(u.ip4) as local_ip4, \
                    INET_NTOA(u.ip5) as local_ip5, \
                    INET_NTOA(u.real_ip) as real_ip, h.number as house, sw.`name` as sw_name, \
                    INET_NTOA(sw.ip) as switch_ip, sw.`comment` as comment, st.`name` as street, u.phone, u.mac_onu, u.real_port \
                    from users as u, switches as sw, houses as h, streets as st \
                    where u.switch = sw.id and u.id="%s" and st.id = h.street and sw.house = h.id' %user_id
cursor.execute(query)
zapros = cursor.fetchall()
#mac_onu = 'None'
#Задаем переменные полученные из запроса в БД Абонентов
if len(zapros)>0:
    for row in zapros:
        username = row[0]
        flat = row[1]
        port_number = row[2]
        vlan_bd = str(row[3])
        local_ip = row[4].decode("utf-8")
        local_ip2 = row[5].decode("utf-8")
        local_ip3 = row[6].decode("utf-8")
        local_ip4 = row[7].decode("utf-8")
        local_ip5 = row[8].decode("utf-8")
        real_ip = row[9].decode("utf-8")
        house = row[10]
        sw_name = row[11]
        sw_ip = row[12].decode("utf-8")
        comment = row[13]
        street = row[14]
        phone = row[15]
        mac_onu = row[16]
        real_port = row[17]
else:
    print ("Неверно задан ID или нет данных в БД Абонентов")
    raise SystemExit



print ("<p><b>ФИО:</b> %s / Телефон: %s" % (username, phone))
print ("<br><b>Адрес:</b>Улица: %s / Дом: %s / Квартира: %s" % (street, house, flat))
#if mac_onu != None or mac_onu != '':

if mac_onu:
    print ("<br><b>MAC ONU:</b> %s" % mac_onu)
else:
    print ("<br><b>Номер порта:</b> %s" % port_number)
    if real_port == None or not real_port:
        pass
    else:
        port_number = real_port
        print ("<br><b>Настоящий номер порта:</b> {}".format(real_port))
print ("<br><b>Vlan из БД абонентов:</b>" +vlan_bd)



#Условия вывода IP адресов
if local_ip == '0.0.0.0':
    pass
else:
    print ("<br><b>Локальный IP:</b> %s" %local_ip)
    if local_ip2 != '0.0.0.0':
        print ("/ "+local_ip2)
    if local_ip3 != '0.0.0.0':
        print ("/ "+local_ip3)
    if local_ip4 != '0.0.0.0':
        print ("/ "+local_ip4)
    if local_ip5 != '0.0.0.0':
        print ("/ "+local_ip5)
if real_ip == '0.0.0.0':
    print ("<br><b>Внешний IP не задан в БД Абонентов</b>")
else:
    print ("<br><b>Внешний IP:</b> %s" % real_ip)


#Получение данных об тарифе IPTV

query = 'select packets.`name` as iptarif \
        from users as u, packets, packets_subscribe \
        where u.id=%s and u.id = packets_subscribe.`user` \
        and packets.id = packets_subscribe.packet' % user_id
cursor.execute(query)
list_iptarif = cursor.fetchall()

sw_dict = {"dlink": ['10.0.9.197', '10.0.9.202', '10.0.9.115'],
           "orion": ['10.0.9.19', '10.0.9.158', '10.0.9.208', '10.0.9.216', '10.0.9.199'],
           "snr": ['10.0.9.125', '10.0.9.177', '10.0.9.178'],
           "bdcom": ['10.0.9.214', '10.0.9.39'],
           "cdata": ['10.0.9.226'],
           "zyxel": ['10.0.9.112', '10.0.9.113', '10.0.9.142', '10.0.9.160', '10.0.9.171', '10.0.9.189']
          }
def dev(v_ip):
    for key, value in sw_dict.items():
        for item in value:
            if item == v_ip:
                return key

sw_type = dev(sw_ip)

#Вызов функции для получения данных с коммутатора доступа
"""
if sw_ip == '10.0.9.19' or sw_ip == '10.0.9.158' or sw_ip == '10.0.9.208':
    model, config, uptime, int_status, macs, igmp_profile, channels = switches.orion(sw_ip, vlan_bd, port_number, user_id)
elif sw_ip == '10.0.9.197' or sw_ip == '10.0.9.202':
    model, config, uptime, int_status, macs, igmp_profile, channels = switches.dlink(sw_ip, vlan_bd, port_number, user_id)
else:
    model, config, uptime, int_status, macs, igmp_profile, channels, errors = switches.cisco2950(sw_ip, vlan_bd, port_number, user_id)
"""
if sw_type == 'orion':
    model, config, uptime, int_status, macs, igmp_profile, channels = switches.orion(sw_ip, vlan_bd, port_number, user_id)
elif sw_type == 'dlink':
    model, config, uptime, int_status, macs, igmp_profile, channels = switches.dlink(sw_ip, vlan_bd, port_number, user_id)
elif sw_type == 'snr':
    model, config, uptime, int_status, macs, errors = switches.snr(sw_ip, vlan_bd, port_number, user_id)
elif (sw_type == 'bdcom'):
    model, config, uptime, int_status, iface, opt_diag, macs = switches.bdcom(sw_ip, mac_onu)
elif (sw_type == 'cdata'):
    model, config, uptime, int_status, iface, opt_diag, macs, onu_status = switches.cdata(sw_ip, mac_onu, vlan_bd)
elif sw_type == 'zyxel':
    model, config, uptime,  int_status, macs, errors = switches.zyxel(sw_ip, port_number)
else:
    model, config, uptime, int_status, macs, igmp_profile, channels, errors, ifload = switches.cisco2950(sw_ip, vlan_bd, port_number, user_id)

print ("<br><br><b>Коммутатор: </b>%s / <b>IP:</b><a href=\"telnet://%s/\" title=\"Открыть коммутатор в консоли\"> %s</a> / <b>Тип:</b>%s  / <b>Время работы:</b>%s<br>" % (sw_name, sw_ip, sw_ip, model, uptime))

#Вывод конфигурации порта
a = """
<div><a onclick="hidetxt('div1'); return false;" href="#" rel="nofollow" title="Раскрыть конфигурацию порта">Конфиг порта</a>
<div style="display:none;" id="div1">
"""
print (a)
# Вывод конфигурации интерфейса
for row in config:
    print(row+"<br>")
print ("<br></div>")
print ("</div>")
# Вывод статуса настройки ONU
#print('ONU status: %s' % onu_status)
if onu_status is not None:
    if onu_status == 1:
        print('<b>ONU настроена правильно</b></br>')
    elif onu_status == 0:
        print('<b>ONU не настроена</b></br>')
        #print('SW_IP: %s, VLAN: %s, MAC: %s' % (sw_ip, vlan_bd, mac_onu))
        forma('cdata_apply_onu', 'fake', 'fake', 'fake', 'fake', sw_ip, 'fake', vlan_bd, mac_onu)


# Вывод загрузки порта
if(ifload):
    print ("<b>Состояние порта:</b><br>"+int_status+"<br>")
    print ("<b>Загрузка порта за последние 30сек:</b><br>Исходящий: %.3f Мбит/сек, %s пакетов/сек" % (float(ifload[0])/1000000, ifload[1]))
    print ("<br>Входящий: %.3f Мбит/сек, %s пакетов/сек<br>" % (float(ifload[2])/1000000, ifload[3]))

#Вывод MAC адреса
def oui_find(mac):
    mac2 = mac.replace('-', ':')
    mac2 = mac2.replace('.', ''); #mac2 = mac2.replace(':', '')
    mac2 = mac2.upper()
    mac2 = mac2[:len(mac2)//2]
    #Split mac on two characters and insert colon (:)
    mac2 = ":".join(re.findall('..', mac2))
    #print(mac2)
    reader = csv.reader(tokenize.open('/var/www/check/cgi-bin/ouibase.csv'), delimiter=',')
    for row in reader:
        if row[0] == mac2:
            print (row[2])

if len(macs) != 0:
    print ("<b>MAC адреса на порту:</b><br>")
    for mac in macs:
        print (mac+" || ")
        oui_find(mac)
        print ("<br>")
else:
    print ("<b>Нет MAC адресов на порту</b><br>")

if opt_diag is not None:
    print ('<b>Мощность сигнала на ONU</b> :'+opt_diag+'<br>')

if errors != 'No':
    print("<b>Ошибки на порту:</b><br>")
    print(errors+"<br>")
    forma('clear_counters', 'fake', 'fake', 'fake', 'fake', sw_ip, port_number)
    forma('offonport', 'fake', 'fake', 'fake', 'fake', sw_ip, port_number)

#else:
#    pass

#Check for local and real IPs'
if local_ip != '0.0.0.0' and real_ip != '0.0.0.0':
    query_ip = local_ip
elif local_ip != '0.0.0.0' and real_ip == '0.0.0.0':
    query_ip = local_ip
else:
    query_ip = real_ip

#print("<br>Query IP :"+query_ip)
#Вывод тарифа IPTV и igmp профиля. Если есть.
if len(list_iptarif) != 0:
    print ("<br><b>Тариф IPTV: </b>")
    for item in list_iptarif:
        print (item[0])
        if len(list_iptarif)>1:
            print(", ")
    print ("<br>")
else:
    print ("<br><b>Нет тарифов IPTV</b><br>")

if 'igmp_profile' in globals():
    if len(igmp_profile) != 0:
        print ("<b>IGMP профиль:</b>")
        for profile in igmp_profile:
            print (profile, ',')
    else:
        print("<b>Нет IGMP профиля</b>")
else:
    print ("<b>Проверка IGMP профиля не производится</b>")

#Какие каналы смотрит
if 'channels' in globals():
    if len(channels) != 0:
        print ("<br><b>Смотрит каналы: </b>")
        i = 0
        for ip_ch in channels:
            query = 'select name from channels where ip = INET_ATON(\'%s\')' % ip_ch
            cursor.execute(query)
            channel = cursor.fetchall()
            i += 1
            print (str(channel[0][0])+"(%s)" % ip_ch)
            #Ставим запятые только между элементами
            if len(channels) > 1:
                if i == len(channels):
                    pass
                else:
                    print(", ")
    else:
        print ("<br><b>Каналы сейчас не смотрит</b>")
else:
    print ("<br><b>Проверка каналов не производится</b>")

#UTM5_521007 connect and select
db = pymysql.connect(host='192.168.11.4', user='utm5', passwd='utm5', db='UTM5_521007', use_unicode='True', charset='utf8')
cursor = db.cursor()

query = 'SELECT ip_groups.mac, convert(cast(convert(tariffs.`name` using latin1) as binary) using utf8), \
        convert(cast(convert(users.full_name using latin1) as binary) using utf8), accounts.balance, accounts.is_blocked, users.basic_account \
        FROM users,accounts,service_links,iptraffic_service_links,ip_groups,account_tariff_link,tariffs \
        WHERE users.is_deleted=0 \
        AND users.basic_account=accounts.id \
        AND account_tariff_link.account_id = users.basic_account \
        AND account_tariff_link.is_deleted=0 \
        AND account_tariff_link.tariff_id = tariffs.id \
        AND account_tariff_link.account_id = accounts.id \
        AND accounts.is_deleted=0 \
        AND accounts.id=service_links.account_id \
        AND service_links.is_deleted=0 \
        AND service_links.id=iptraffic_service_links.id \
        AND iptraffic_service_links.is_deleted=0 \
        AND iptraffic_service_links.ip_group_id=ip_groups.ip_group_id \
        AND ip_groups.is_deleted=0 \
        AND inet_ntoa(ip_groups.ip & 0xFFFFFFFF)="%s"' % query_ip
cursor.execute(query)
print ("<h3>Проверка правильности настроек абонента в UTM, Cisco 4948</h3>")
zapros = cursor.fetchall()
#Check query for existing tarif, full_name and etc.
#print(zapros)
down_speed,down_sec,up_speed,up_sec,sh_status = services.check_speed(real_ip)
if len(zapros)>0:
    for row in zapros:
        vlan = row[0]
        tarif = row[1]
        username = row[2]
        balance = '%.2f'%(row[3])
        lock = row[4]
        account = row[5]
        if vlan[-2] == '_':
            vlanutm = vlan[4:-2]
        else:
            vlanutm = vlan[4:]
#        print (username+"</br>")
#        print("IP адрес:<b> "+real_ip+"</b><br>")
        print("Лицевой счет:<b> "+str(account)+"</b><br>")
        print("VLAN UTM:<b> "+vlan+"</b><br>")
        if '_2' in vlan:
            helper_address = '10.0.100.18'
        else:
            helper_address = '10.0.100.9'
        print("Тариф UTM:<b> "+tarif+"</b><br>")
        print("Баланс на счету:<b> "+str(balance)+"</b><br>")
        if down_speed == 'not_exist':
            print("Нет тарифа на шейпере. На счету минус или не заведен тариф в UTM<br>")
        else:
            print("Скорость на шейпере Входящий/Исходящий, Мбит/сек: <b>", down_speed, '/', up_speed,'</b><br>')
            if sh_status == 'off':
                print("Интернет на шейпере <b>ВЫКЛЮЧЕН</b><br>")
            elif sh_status == 'on':
                print("Интернет на шейпере <b>ВКЛЮЧЕН</b><br>")
            print("Сколько секунд назад был последний Входящий/Исходящий пакет: <b>", down_sec, '/', up_sec, '</b>')
#        print ("<br><b>Vlan из UTM:</b>" +vlanutm)
        if lock == 16:
            print ("  (Системная блокировка)<br>")
        elif lock == 0:
            print ("<br>")
        else:
            print ("  (Админская блокировка)<br>")
else:
    print ("Для этого IP нет ни одной связки в UTM (<i>Или кончился промо период или удалена сервисная связка</i>)<br>")
#########################################################################################
"""
sm = "10.3.0.240"
user = "pcube"
user_pw = "Ybrnjrhjvtyfc"
#real_ip = "31.130.123.180"

#Check current tarif on SCE
child = pexpect.spawn ('ssh -o \"StrictHostKeyChecking no\" %s@%s' % (user, sm))
child.timeout = 4
#child.expect ('password:')
#child.sendline (user_pw)
child.expect ('.*pcube@sm.*')
child.sendline ('/opt/pcube/sm/server/bin/p3subs --show --ip=%s' % real_ip)
child.timeout = 3
child.expect ('\$')
subs = child.before
subs2 = subs.decode("utf-8").split('\n')
child.sendline ('exit')

for line in subs2:
    if re.findall(r'packageId', line):
        result = re.findall('\d+', line)
        if result[0] == '1':
            print("Тариф на SCE: <b>Интернет выключен!</b>")
        else:
            query = 'select convert(cast(convert(service_name using latin1) as binary) using utf8) from services_data where id ="%s"' % result[0]
            cursor.execute(query)
            for row in cursor.fetchall():
                tarif_sce = row[0]
                print("Тариф на SCE:<b> "+tarif_sce+"</b><br>")
    elif re.findall(r'No subscriber exists', line):
        print ("<b>Для этого абонента нет тарифа на SCE</b><br>")
#        raise SystemExit
"""
#########################################################################################
db.close()

if local_ip != '0.0.0.0':
    aggregator = None
    aggregator = aggreg.check_agg_local(local_ip)[0]
    routerHostname = aggreg.check_agg_local(local_ip)[1]
    loopback = aggreg.check_agg_local(local_ip)[2]
    vlan = vlan_bd
    print ("<br><b>Внимание!!! Абонент на NAT</b>")
    print ("<br>Требуемый loopback для "+local_ip+": <b>"+loopback+"</b><br>")
else:
    aggregator = None
    aggregator = aggreg.check_agg(real_ip)[0]
    routerHostname = aggreg.check_agg(real_ip)[1]
    loopback = aggreg.check_agg(real_ip)[2]
    print ("<br>Требуемый loopback для "+real_ip+": <b>"+loopback+"</b><br>")

if aggregator is not None:
    print ("Аггрегирующий коммутатор: <b>" + aggregator + "</b>")

user = "service"
password = "1081978"
enablepassword = "ybrnjrhjvtyfc"

#Check policy for interface
policy = checkpolicy(real_ip)
print ("<br><h3>Настройки абонентского интерфейса VLAN на "+aggregator+"<br></h3><hr align=\"left\" width=\"370\">")

#print("<p><font color='red'>Для сетей 31.130.123.0/24, 31.130.121.0/24, 95.66.228.0/24 на VLAN интерфейсе должен быть: ip policy route-map INET_CHANNEL2<br>")
#print("Для сети 91.237.209.0/24 должен быть ip policy route-map INET_BGP2</font></p>")

#Output interface settings
#vlan = re.findall('\d+', vlan)[0]
vlan = vlanutm
####
#Place for forma function
####


if vlan is not None:
#Connect to cisco and execute commands
################################################
        child = pexpect.spawn ('telnet '+aggregator)
        child.expect ('Username: ')
        child.sendline (user)
        child.expect ('Password: ')
        child.sendline (password)
        child.expect (routerHostname+'>')
        child.sendline ('enable')
        child.expect ('Password: ')
        child.sendline (enablepassword)
        child.expect (routerHostname+'#')

        #Check vlan in DHCP snooping base
        child.sendline ('terminal length 300')
        child.expect (routerHostname+'#')
        child.sendline ('sh ip dhcp snooping | begin VLANs')
        child.expect (routerHostname+'#')
        dirt = child.before.strip()
        dirt = dirt.decode('ascii').split('\n')
        diapazon = dirt[2]
        diapazon = diapazon.split(',')
        snoop_vlans = []
        for item in diapazon:
            if '-' in item:
                x, y = item.split('-')
                for item in range(int(x), int(y)+1):
                    snoop_vlans.append(item)
            else:
                snoop_vlans.append(int(item))
        #Check vlan in snooping base list
        if int(vlan) in snoop_vlans:
            print('<p> <font color="green">Vlan' +vlan+ ' в DHCP Snooping\'е.  Всё ОК!</font></p>')
        else:
            print('<p> <font color="red">VLAN не в DHCP Snooping!!! Надо добавить на Cisco 4948 [Cisco4948(config)#ip dhcp snooping vlan '+vlan+']</font></p>')
        #Check int vlan settings
        child.sendline ('sh run int vlan %s' % vlan)
        child.expect (routerHostname+'#')
        intface = child.before.strip()
#        child.sendline ('exit')
        #Split binding
        shrunint = intface.decode('ascii').split('\n')
        shrun = shrunint[5:]
        #Check that interface is exist
        if len(shrun) == 0:
            print('<p><font color="red">Интерфейс для этого VLAN не существует. Его надо создать.</font></p>')
            
            forma('create_int', loopback, helper_address, 'fake', policy, 'fake', 'fake', vlan, 'fake')
        current_loopback = ''
        current_helper_address = ''
        current_policy = ''
        for line in shrun:
            if 'no' in line:
                pass
            elif 'end' in line:
                pass
            else:
                if 'Loopback' in line:
                    current_loopback = line.split()[2].lower()
                elif 'helper-address' in line:
                    current_helper_address = line.split()[2]
                elif 'policy' in line:
                    current_policy = line.rstrip()[1:]
                print (line+"<br>")
        #Check helper addres on interface
        if helper_address == current_helper_address:
            pass
            #print('Helper-address правильный')
        else:
            if current_helper_address:
                print('<p><font color="red">Helper-address не правильный '+current_helper_address+' . Должен быть '+helper_address+'. Надо исправить</font></p>')
                forma('change_helper', 'fake', helper_address, current_helper_address, 'fake', 'fake', 'fake', vlan, 'fake')
        #Check loopback
        if loopback == current_loopback:
            print('<p><font color="green">Loopback правильный</font><p>')
        else:
            #Check current loopback in vlan interface
            if current_loopback:
                print('<p><font color="red">Loopback на интерфейсе не правильный. Надо исправить</font></p>')
                print("VLAN = %s<br>" % vlan)
                forma('change_loopback', loopback, 'fake', 'fake', 'fake', 'fake', 'fake', vlan, 'fake')
        #Check policy
        if policy == current_policy:
            print('<font color="green">Policy правильный</font>')
        elif policy == '':
            policy = 'no '+current_policy
            print('<font color="red">На этом интерфейсе не должно быть никаких policy!</font><br>')
            forma('create_policy', 'fake', 'fake', 'fake', policy, 'fake', 'fake', vlan, 'fake')
        else:
            if current_policy:
                #print("<br>--"+current_policy+"--")
                #print("<br>--"+policy+"--")
                print('<font color="red">Текущий policy не правильный! Должен быть: '+policy+'</font><br>')
                forma('create_policy', 'fake', 'fake', 'fake', policy, 'fake', 'fake', vlan, 'fake')
            else:
                print('<font color="red">Нет policy на интерфейсе! Должен быть: '+policy+'</font><br>')
                forma('create_policy', 'fake', 'fake', 'fake', policy, 'fake', 'fake', vlan, 'fake')
        #Current binding
        child.sendline ('sh ip dhcp snooping binding vlan %s' % vlan)
        child.expect (routerHostname+'#')
        bind = child.before.strip()
        child.sendline ('exit')
        #Split binding
        #link = bind.decode('ascii').split('\n')[3]
        link = bind.decode('ascii').split('\n')
        print ("</br>")
        print ("<b>Текущие связки на "+aggregator+"</b></br>")
        for row in link[3:-1]:
            print (row+"<br>")


print ("<p><a href=\"http://check.office.net/cgi-bin/check/cisco_python.py?userid=%s&vlan=%s&real_ip=%s&switch_ip=%s&port_number=%s\" \
target=\"_blank\">Сбросить связку</a></p>" % (user_id, vlan, real_ip, sw_ip, port_number))

#Show Netflow records
print("<br><b>Исходящий трафик по абоненту за последние 10 минут. Вывод по 20 записей.</b>")
nf = services.nfdump(real_ip)
print('<table cellspacing="0" border="1" cellpadding="2">')
print("<tr><td><b>Дата</b></td><td>Время</td><td><b>Длит.</b></td><td><b>Протокол</b></td><td><b><b>IP источник</b></td><td></td><td><b>IP назначения</b></td><td><b>Пакетов</b></td><td><b>Байт</b></td><td><b>Потоков</b></td></tr>")
for line in nf[1:-5]:
    print("<tr>")
    for item in line.split():
        print("<td>&nbsp;&nbsp;"+item+"</td>")
    print("</tr>")
print("</table>")

print ("<p>&nbsp;</p><p align=\"center\">CheckUsers Version:3.2   Powered by Python3</p>")
t2 = '%.2f' % (time.time()-t1)
print ("Время выполнения скрипта: %s" % t2 )
print ("</body>")
print ("</html>")
