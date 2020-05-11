#!/usr/bin/env python3
import time
import json
import requests
import urllib3
import pprint
import tabulate
requests.packages.urllib3.disable_warnings()

#función que pide nuevos tickets, la variable donde se guarda el ticket es global
def cons_Ticket():
    global ticket
    api_url="https://devnetsbx-netacad-apicem-3.cisco.com/api/v1/ticket"
    headers={
        "content-type":"application/json"
    }
    body_json={
        "username":"devnetuser",
        "password":"Xj3BDqbU"
    }
    resp=requests.post(api_url,json.dumps(body_json),headers=headers,verify=False)
    response_json = resp.json()
    if resp.status_code==200:
        print("Ticket conseguido:",response_json["response"]["serviceTicket"])
        ticket = response_json["response"]["serviceTicket"]
    else:
        raise Exception ("Error consiguiendo ticket: " + resp.text)
#funcíon que hace las peticiones, es capaz de pedir un ticket si no lo hay o de repetirse una vez si hay algun error con el ticket, la variable rep es para evitar bucles infinitos
def cons_resp(uRL,rep=0):
    if ticket==None:
        print("No hay ticket, consiguiendo ticket")
        cons_Ticket()
    api_url = "https://devnetsbx-netacad-apicem-3.cisco.com/api/v1/"+uRL
    headers = {
     "content-type": "application/json",
     "X-Auth-Token": ticket
    }
    resp = requests.get(api_url, headers=headers, verify=False)
    if resp.status_code != 200:
        if resp.status_code == 401 and rep==0:
            print("posible error con ticket, consiguiendo nuevo ticket")
            cons_Ticket()
            return cons_resp(uRL,1)
        else :
            print("Error en petición: "+ str(resp.status_code) + "\n" + resp.text)
            input("pulse enter para continuar")
            return None
    return resp.json()
#función que toma la petición y la muestra, los valores extra son necesarios para algunas de las distintas peticiones
def vision_resumida_host(peti,endp,ip):
    lista=[]
    if endp ==1:
        for i in range (len(peti["response"])):
            lista.append( [i+1,peti["response"][i]["hostType"],peti["response"][i]["hostIp"]] )
        table_header = ["Numero", "Type", "IP"]
    elif endp==2:
        for i in range (len(peti["response"])):
            lista.append([i+1,peti["response"][i]["ipv4Address"],peti["response"][i]["macAddress"],peti["response"][i]["speed"],peti["response"][i]["interfaceType"]])
        table_header = ["Numero", "IPv4", "MAC","Velocidad","Tipo"]
    elif endp==3:
        for i in range(len(ip)):
            lista.append([ip[i],peti["response"][ip[i]]["city"],peti["response"][ip[i]]["country"],peti["response"][ip[i]]["continent"]])
        table_header=["IP", "ciudad","pais","continente"]
    elif endp==4:
        for i in range (len(peti["response"])):
            lista.append([i+1,peti["response"][i]["family"],peti["response"][i]["serialNumber"],peti["response"][i]["hostname"],peti["response"][i]["managementIpAddress"],peti["response"][i]["errorCode"]])
        table_header=["Numero","Familia","Numero de serie","Hostname","Ip de gestion","Errores"]
    print(tabulate.tabulate(lista, table_header))
#función capaz de parciarmente leer la petición y listar al usuarios que atributos quiere ver
def vision_personalizada(peti,endp,ip):
    cualid=[]
    if endp == 3:
        for i in ip:
            for j in peti["response"][i].keys():
                if j not in cualid:
                    cualid.append(j)

    else:  
        for i in peti["response"]:
            for j in i.keys():
                if j not in cualid:
                    cualid.append(j)
    print("Bienvenidos a visión personalizada, introduzca de la siguiente lista que atributos quiere ver")
    cualidAVer=[]
    while True:
        print(cualid)
        print("introduzca 0 para para Terminar")
        if len(cualidAVer)>0:
            print ("Atributos introducidos:",cualidAVer)
        inp=input("introduzca una atributo: ")
        if inp =="0":
            print ("Hemos terminado")
            break
        if inp not in cualid:
            print ("atributo no reconocida, intente de nuevo")
            time.sleep(1)
            continue
        elif inp in cualidAVer :
            print ("atributo ya introduzido")
            time.sleep(2)
            continue
        else:
            cualidAVer.append(inp)
    if len (cualidAVer)==0:
        print("No se han introducido cualidades")
        return None
    elif endp==3:
        lista=[]
        for i in range(len(peti["response"])):
            host=[ip[i]]
            for item in cualidAVer:
                if item in peti["response"][ip[i]]:
                    host.append(peti["response"][ip[i]][item])
                else:
                    host.append("N/A")
            lista.append(host)
    else:
        lista=[]
        for i in range (len(peti["response"])):
            host=[]
            host.append(i+1)
            for item in cualidAVer:
                if item in peti ["response"][i].keys():
                    host.append(peti["response"][i][item])
                else:
                    host.append("N/A")
            lista.append(host)
        cualidAVer.insert(0,"Numero")
    print( tabulate.tabulate(lista, cualidAVer) )
#Pricipio del codigo

ip=None
ticket=None
peti=None
while True:#menu principal
    print("""
    Menu-Script test API-CEM
    1-Ver inventario
    2-Ver interfaces
    3-Localizar IP publica
    4-Ver dispositivos de red
    5-Introducir ticket
    6-Conseguir ticket
    0-Salir
    """)
    if peti != None:
        print("Hay una respuesta Guardada, introduzca 9 para ver")
    if ticket !=None:
        print("Tenemos un Ticket:",ticket)
    input1=input("Seleccione una opción: ")
    if input1 =="1":
        peti=cons_resp("host")
        endp=1
    elif input1 == "2":
        peti=cons_resp("interface")
        endp=2
    elif input1=="3":
        ip=input("Introduzca cualquier numero de Ips a localizar, si introduce multiples, separelas con un espacio: ")
        peti=cons_resp("ipgeo/"+ip)
        endp=3
        ip=ip.split()
    elif input1 =="4":
        peti=cons_resp("network-device")
        endp=4
    elif input1 == "5":
        ticket=input("Por favor introduzca ticket: ")
        continue
    elif input1 == "6":
        cons_Ticket()
        continue
    elif input1=="0":
        print("Adios y gracias")
        break
    elif input1=="9" and peti!= None:
        pass
    else:
        print ("input no reconocido, intente de nuevo")
        time.sleep(2)
        continue
    if peti == None:
        continue
    while True:#menu de visualización
        print("""
    Visulizador: ¿Como desea ver la respuesta?
    1-Resumido
    2-Raw
    3-Personalizada
    0-Volver a menu principal
        """)
        input2=input("Seleccione una accion: ")
        if input2=="1":
            vision_resumida_host(peti,endp,ip)
            input("Pulse enter para continuar")
        elif input2=="2":
            pprint.pprint (peti)
            input("Pulse enter para continuar")
        elif input2=="3":
            vision_personalizada(peti,endp,ip)
            input("Pulse enter para continuar")
        elif input2=="0":
            print ("Volviendo a menu principal")
            time.sleep(1)
            break
        else:
            print ("Input no reconocido")
