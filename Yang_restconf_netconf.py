#!/usr/bin/env python3
from netmiko import ConnectHandler
import json
import requests
import urllib3
from pprint import pprint
from tabulate import tabulate
requests.packages.urllib3.disable_warnings()

baseurl="ios-xe-mgmt.cisco.com"
puertos=[8181,9443]
basicauth=["developer","C1sco12345"]

def conect_shh(baseurl,port,basicauth):#una conexion SSH basica enganchada en el script
    try:
        sshcli=ConnectHandler(baseurl,device_type="cisco_ios", port=port,username=basicauth[0],password=basicauth[1])
        print("conectados a",baseurl)
        while True:
            comando=input("Introduzca un comando o Salir para salir:")
            if comando=="Salir":
                return
            output=sshcli.send_command(comando)
            print(output)
    except Exception as e :
        print("Error con conexión:\n",e)
        return
def config():#una funcion para configurar los distintos parametros
    global baseurl
    global puertos
    global basicauth
    while True:
        print("Configuración:\n-Host remoto:",baseurl,"\nPuertos:\n-SSH:",puertos[0],"\n-Netconf:",puertos[1],"\nSeguridad:\n-Usuario:",basicauth[0],"\nContraseña:",basicauth[1])
        print("""
    ¿Que se va a configurar?
    1-Host remoto
    2-Puertos
    3-Autentificación
    0-Volver
        """)
        seleccion2=input("introduzca opción: ")
        if seleccion2=="1":
            print("Host remoto",baseurl)
            baseurl=input("Introduzque nuevo host: ")
            continue
        elif seleccion2=="2":
            print("Puertos:\n1-SSH:",puertos[0],"\n3-Restconf",puertos[1])
            seleccion3=input("Seleccione puerto a cambiar y nuevo puerto separados por un espacio.Ej:para cambiar el puerto ssh a 80: '1 80'")
            seleccion3=seleccion3.split()
            try:
                puertos[seleccion3[0]]=seleccion3[1]
                continue
            except Exception as a:
                print("ha sucedido un error:",a)
                continue
        elif seleccion2=="3":
            print("Usuario",basicauth[0],"\nContraseña",basicauth[1])
            basicauth[0]=input("Introduza el nuevo usuario: ")
            basicauth[1]=input("Introduza la nueva contraseña: ")
            continue
        elif seleccion2=="0":
            return
        else:print ("Selección no reconocida")

def restConect(baseurl,port,basicauth,resource):#Esta función hace las peticiones de Restconf, distintos valores en resource significan diferentes maneras de manejar las peticiones y respuestas
    resturl="https://"+baseurl+":"+str(port)
    headers={
        "Accept":"application/yang-data+json",
        "Content-type":"application/yang-data+json"
    }
    basicautht=tuple(basicauth)#a resquests no le gustan las listas
    if resource==4:
        inputs=[]
        inputs.append(input("nombre de la interfaz: "))
        inputs.append(input("descripción: "))
        inputs.append(input("tipo(iana-if-type:softwareLoopback,iana-if-type:ethernetCsmacd): "))
        inputs.append(input("IP: "))
        inputs.append(input("Mascara: "))
        yang_Config={"ietf-interfaces:interface":{
            "name":inputs[0],
            "description":inputs[1],
            "type":inputs[2],
            "enabled":True,
            "ietf-ip:ipv4":{
                "address":[
                    {
                        "ip":inputs[3],
                        "netmask":inputs[4]
                    }
                ]
            },
            "ietf-ip:ipv6":{}
        }}
        try:
            resul=requests.put(resturl+"/restconf/data/ietf-interfaces:interfaces/interface="+inputs[0],data=json.dumps(yang_Config), auth=basicautht, headers=headers, verify=False)
            if (resul.status_code >= 200 and resul.status_code <= 299):
                print("STATUS OK: {}".format(resul.status_code)) 
            else: 
                print("Error code {}, reply: {}".format(resul.status_code, resul.json()))
            return
        except Exception as e:
            print("A surgido un error:\n", e)
            return
    if resource ==5:
        interface=input("Interfaz a borrar: ")
        try:
            resul=requests.delete(resturl+"/restconf/data/ietf-interfaces:interfaces/interface="+interface, auth=basicautht, headers=headers, verify=False)
            if (resul.status_code >= 200 and resul.status_code <= 299):
                print("STATUS OK: {}".format(resul.status_code)) 
            else: 
                print("Error code {}, reply: {}".format(resul.status_code, resul.json()))
            return
        except Exception as e:
            print("A surgido un error:\n", e)
            return
    if resource==6:
        respuesta = requests.get(resturl+"/restconf/data/netconf-state/capabilities", auth=basicautht, headers=headers, verify=False)
        respuesta_json = respuesta.json()
        pprint(respuesta_json)
        input("Pulse enter para continuar")
        return
    if resource ==7:
        respuesta = requests.get(resturl+"/restconf/data/ietf-interfaces:interfaces-state", auth=basicautht, headers=headers, verify=False)
        respuesta_json = respuesta.json()
        interfaces=[]
        for item in respuesta_json ["ietf-interfaces:interfaces-state"]["interface"]:
            interfaces.append([item["name"],item["speed"],item["oper-status"],])
        cabecera=["Interfaz","velocidad","Estado"]
        print(tabulate(interfaces,cabecera))
        input("pulse enter para continuar")
        return
    respuesta = requests.get(resturl+"/restconf/data/ietf-interfaces:interfaces", auth=basicautht, headers=headers, verify=False)
    respuesta_json = respuesta.json()
    respuesta2=requests.get(resturl+"/restconf/data/ietf-interfaces:interfaces-state", auth=basicautht, headers=headers, verify=False)
    respuesta2_json=respuesta2.json()
    interfaces=[]
    for item in respuesta_json["ietf-interfaces:interfaces"]["interface"]:
        for item2 in respuesta2_json["ietf-interfaces:interfaces-state"]["interface"]:
            if item["name"]==item2["name"]:
                mac=item2["phys-address"]
        interfaces.append([item["name"],item["ietf-ip:ipv4"],mac])#Aqui no puedo sacar la IP, por alguna razon me da error: KeyError: 'address' , pero estoy usando la llave correcta
    cabecera=["nombre","IP","MAC"]
    print(tabulate(interfaces,cabecera))
    input("pulse enter para continuar")

while True:#Menu principal
    print("Configuración:\n-Host remoto:",baseurl,"\nPuertos:\n-SSH:",puertos[0],"\n-Restconf:",puertos[1])
    print("""
    1-Configuración
    2-CLI SSH
    3-Conseguir interfaces
    4-Crear/updatear interfaces
    5-Borrar interfaces
    6-Conseguir capacidades restconf
    7-Estado de las interfaces
    0-Salir
    """)
    seleccion=input("Selecione una opción: ")
    if seleccion=="1":
        config()
        continue
    elif seleccion=="2":
        conect_shh(baseurl,puertos[0],basicauth)
        continue
    elif seleccion=="3":
        restConect(baseurl,puertos[1],basicauth,3)
        continue
    elif seleccion=="4":
        restConect(baseurl,puertos[1],basicauth,4)
        continue
    elif seleccion=="5":
        restConect(baseurl,puertos[1],basicauth,5)
        continue
    elif seleccion=="6":
        restConect(baseurl,puertos[1],basicauth,6)
        continue
    elif seleccion=="7":
        restConect(baseurl,puertos[1],basicauth,7)
        continue
    elif seleccion=="0":
        break