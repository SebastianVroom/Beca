import time
def prioridad(elem):#función para un sort
    if elem[1]=="**":return 1
    elif  elem[1]=="*":return 2
    elif  elem[1]=="/":return 3
    elif  elem[1]=="+":return 4
    elif  elem[1]=="-":return 5
def pelar_parentesis(cad):#Detecta parentesis dentro de una cadena, los trocea y coloca el resulrado en una lista
    recur=False
    resul=[]
    i=0
    oper=""
    if cad.count("(")==cad.count(")"):
        while True:
            if cad[i]=="(":
                count =1
                oper+="?"
                paren=cad[i+1:]
                for j in range (len(paren)):
                    if paren[j]=="(":
                        count+=1
                    elif paren[j]==")":
                        count-=1
                    if count>1: recur=True
                    if count==0:
                        paren=paren[:j]
                        i=i+j+1
                        break
                if recur:
                    paren=pelar_parentesis(paren)
                    recur=False
                resul.append(paren)
            else: oper+=cad[i]
            i+=1
            if i >=len(cad):
                break
        resul.append(oper)
        return resul
    else:
        return None
def extraer_operadores(cad):#función que extrae operadores de una cadena y los devuelve en forma de lista junto con su posicón en la expresión
    pos=0
    resul=[]
    for i in range(len(cad)):
        if cad[i] =="+":
            resul.append([pos,"+"])
            pos+=1
        elif cad[i] =="-":
            if not (i==0 or not(cad[(i-1)]=="0" or cad[(i-1)]=="1" or cad[(i-1)]=="2" or cad[(i-1)]=="3" or cad[(i-1)]=="4" or cad[(i-1)]=="5" or cad[(i-1)]=="6" or cad[(i-1)]=="7" or cad[(i-1)]=="8" or cad[(i-1)]=="9")):
                resul.append([pos,"-"])
                pos+=1
        elif cad[i] =="*":
            if cad[i-1]=="*":
                del resul[-1]
                resul.append([(pos-1),"**"])
            else:
                resul.append([pos,"*"])
                pos+=1
        elif cad[i] =="/":
            resul.append([pos,"/"])
            pos+=1
    resul.sort(key=prioridad)#organiza el orden de los operadores segun su prioridad matematica
    return resul
def extraer_numeros(cad):#función que extrae numeros de una cadena
    resul=[]
    num=""
    unineg=False
    for i in range(len (cad)):
        if cad[i]=="-":
            if i==0 or not(cad[(i-1)]=="0" or cad[(i-1)]=="1" or cad[(i-1)]=="2" or cad[(i-1)]=="3" or cad[(i-1)]=="4" or cad[(i-1)]=="5" or cad[(i-1)]=="6" or cad[(i-1)]=="7" or cad[(i-1)]=="8" or cad[(i-1)]=="9"):
                num+="-"
                unineg=True
        if cad[i]=="0" or cad[i]=="1" or cad[i]=="2" or cad[i]=="3" or cad[i]=="4" or cad[i]=="5" or cad[i]=="6" or cad[i]=="7" or cad[i]=="8" or cad[i]=="9":
            num+=cad[i]
        elif cad[i]=="A" and cad[i+1]=="n" and cad[i+2]=="s":
            num=ans
        elif cad[i]=="." and (cad[i-1]=="0" or cad[i-1]=="1" or cad[i-1]=="2" or cad[i-1]=="3" or cad[i-1]=="4" or cad[i-1]=="5" or cad[i-1]=="6" or cad[i-1]=="7" or cad[i-1]=="8" or cad[i-1]=="9")and(cad[i+1]=="0" or cad[i+1]=="1" or cad[i+1]=="2" or cad[i+1]=="3" or cad[i+1]=="4" or cad[i+1]=="5" or cad[i+1]=="6" or cad[i+1]=="7" or cad[i+1]=="8" or cad[i+1]=="9"):
            num+=cad[i]
        else:
            if num != "" and not unineg:
                resul.append(float(num))
                num=""
        unineg=False
    else:
        if num!="":
            resul.append(float(num))
    return resul
def procesado_expresion(cad):#Realiza las operaciónes en las cadenas usando las funciones de extracción
    oper=extraer_operadores(cad)
    nums=extraer_numeros(cad)
    ctrlpos=[]#apunta las posiciones de los operadores ya procesados
    while (len(nums)-1):#procesa las dos cadenas segun la prioridad de los operadores, va borrando elementos de las listas segun las procesa, hasta que solo queda el resultado final
        varpos=0 
        if len(ctrlpos)>0:
            for i in ctrlpos:
                if oper [0][0]>i:
                    varpos+=1
        if oper[0][1]=="**":
            nums[oper[0][0]-varpos]**=nums[(oper[0][0]-varpos)+1]
            del nums[(oper[0][0]-varpos)+1]
            ctrlpos.append(oper[0][0])
        elif oper[0][1]=="*":
            nums[oper[0][0]-varpos]*=nums[(oper[0][0]-varpos)+1]
            del nums[(oper[0][0]-varpos)+1]
            ctrlpos.append(oper[0][0])
        if oper[0][1]=="/":
            nums[oper[0][0]-varpos]/=nums[(oper[0][0]-varpos)+1]
            del nums[(oper[0][0]-varpos)+1]
            ctrlpos.append(oper[0][0])
        if oper[0][1]=="+":
            nums[oper[0][0]-varpos]+=nums[(oper[0][0]-varpos)+1]
            del nums[(oper[0][0]-varpos)+1]
            ctrlpos.append(oper[0][0])
        if oper[0][1]=="-":
            nums[oper[0][0]-varpos]-=nums[(oper[0][0]-varpos)+1]
            del nums[(oper[0][0]-varpos)+1]
            ctrlpos.append(oper[0][0])
        del oper[0]
    else:
        return nums[0]
def strsust (cad,insrt,pos):#funcion para operar en cadena,(Si hice la calculadora antes de terminar el capitulo de python en cadenas)
    return cad[:pos]+insrt+cad[pos+1:]
def control_expresion(lis):#recibe la lista resultada de la función pelar_parentesis y la procesa elemento a elemento
    if isinstance(lis,str):
        return procesado_expresion(lis)
    if len(lis)>1:
        lisPos=[]
        for i in range(len(lis)-1):
            if isinstance(lis[i],list):
                lis[i] = str(control_expresion(lis[i]))
            else:
                lis[i]=str(procesado_expresion (lis[i]))
        for i in range(len(lis[-1])):
            if lis [-1][i]=="?":
                lisPos.append([i,lis[0]])
                del lis[0]
        lisPos.sort(reverse=True)
        for i in lisPos:
            lis[0]=strsust(lis[0],i[1],i[0])
    return  procesado_expresion(lis[0])
ans = None
while True:#menu principal
    try:
        print("""
        Calculadora experimental:
        opciones:
        + Suma
        - Resta
        * Multiplicación
        / División
        ** Exponenciales/Raices
        """)
        if ans != None:
            print("El resultado de la operacion anterior es:",ans)
        cad=input("""
        Introduzca una expresion completa y sera procesada, parentesis incluidos, no omita ningun operador matematico y use los indicados en la lista,
        introduzca 'Ans' dentro de la expresión para usar el ultimo numero calculado, cualquier caracter extraño sera ignorado, pero evite usarlos de todas formas.
        Escriba 'Salir' para salir: 
        """)
        if cad=="Salir":
            print ("Adios")
            break
        cad=cad.replace("?","")
        if "("in cad:
            cad=pelar_parentesis(cad)
            if cad==None:
                print ("Error con parentesis, introduzaca todos los parentesis necesarios")
                time.sleep(4)
                continue
        ans=control_expresion(cad)
        print ("el resultado es:", ans)
        time.sleep (4)
    except TypeError:
        print ("Algo salio mal, ¿Esta seguro de que existe una operacion previa?")
        time.sleep(6)
    except:
        print ("Algo salio mal, intente de nuevo, recuerde no omitir ningun operador en su expresion")
        time.sleep(6)