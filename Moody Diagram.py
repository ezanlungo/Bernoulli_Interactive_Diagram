# -*- coding: utf-8 -*-
"""
Created on Sun May 31 18:53:17 2020

@author: EZEQUIEL
"""


import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

xx1=np.geomspace(1e-6, 1e-5, 2)
xx2=np.linspace(1e-4, 9e-4, 9)
xx3=np.linspace(1e-3, 9e-3, 9)
xx4=np.linspace(1e-2, 1e-1, 10)
RugRel=np.concatenate((xx1, xx2, xx3, xx4))
Re=np.geomspace(4000 ,1e9, 100)
ReL=np.linspace(400, 2300, 20)
ReTrabajo = float(input("Ingrese el Reynolds de trabajo: "))
RugRelTrabajo = float(input("Ingrese la Rugosidad Relativa de trabajo: "))

def factor_friccion(Re, RugRel):
    
    lam= lambda Re: 64.0/Re
    
    def turb(Re, RugRel):
        ffinicial=1.0
        a=2.51*(1/Re)
        b=RugRel/3.7
        # x=1/np.sqrt(ffinicial)
        
        
        y= lambda x: x+2.0*np.log10(b+a*x)
        
        derivy= lambda x: 1+2*(1/(b+a*x))*(a/np.log(10.0))
   
        def NR(x,y,derivy):
            tol=1e-12
            maxiter=5000
            i=1
            X0=ffinicial
            while i<maxiter:
                Xnue=X0-y(X0)/derivy(X0)
                if abs((Xnue-X0))<tol:
                    break
                X0=Xnue 
    
                i=i+1
            return X0

        raiz=NR(ffinicial,y,derivy)
        ff=(1.0/raiz)**2
        return ff

    if Re<=0:
        return print('\n ERROR. Ingrese un Reynolds válido')
    if Re>0 and Re<=2300:
        return lam(Re)
    if Re>4000:
        return turb(Re,RugRel)
    if Re>2300 and Re<=4000:
        return turb(Re,RugRel)

       
vectores=[]
ffturb = np.array([])
for i in range (len(RugRel)):
    Yturb=factor_friccion(1600/RugRel[i], RugRel[i])
    ffturb=np.append(ffturb, Yturb)
for i in range (len(RugRel)):
    ff = np.array([])
    for j in range (len(Re)):
        Y=factor_friccion(Re[j],RugRel[i])
        ff=np.append(ff, Y)
    vectores.append(ff)

fftrabajo = np.array([])
for i in range (len(Re)):
    Y=factor_friccion(Re[i],RugRelTrabajo)
    fftrabajo=np.append(fftrabajo,Y)
    
    
fig,ax=plt.subplots()
ax2 = ax.twinx()
conversion_eje_y=[]
for i in range (len(RugRel)):
    ax.loglog(Re,vectores[i])
    conversion_eje_y.append(factor_friccion(Re[-1],RugRel[i]))
ax2.yaxis.set_tick_params(which='major', size=5, width=1, direction='in', labelsize=5)
ax2.set_yscale("log")
ax2.set_ylim(conversion_eje_y[0],conversion_eje_y[-1])
ax2.set_yticks(conversion_eje_y)
ax2.set_yticklabels(np.round(RugRel,6))    
ax.grid(True, color='0.7', linestyle='-', which='both', axis='both') #No ploteo el ax2 porque en el eje y necesito la grilla de factor de fricción y no de e/D, para e/D uso las curvas con sus respectivas ticks
ax.set_xlabel(r"Reynolds (Re)")
ax.set_ylabel("Factor de Friccion (ff)")
ax2.set_ylabel("Rugosidad Relativa (e/D)") 
ax.set_xlim(ReL[0],Re[-1])   
ax.set_ylim([factor_friccion(Re[-1],RugRel[0]),factor_friccion(Re[-1],RugRel[-1])])
ax.set_title('Diagrama de Moody', fontsize=11, verticalalignment='bottom')    
plt.plot(ReL,64/ReL)
plt.plot(1600/RugRel,ffturb, color='gray', linestyle='dashed')

if ReTrabajo <= 2300 and ReTrabajo > 0:
    plt.plot(ReTrabajo, factor_friccion(ReTrabajo,RugRelTrabajo), 'ko')
    print('\n Régimen laminar, el factor de fricción es: ', factor_friccion(ReTrabajo,RugRelTrabajo), '\n')
if ReTrabajo > 4000: 
    plt.plot(Re,fftrabajo, linestyle='dashed', color='black')
    plt.plot(ReTrabajo, factor_friccion(ReTrabajo,RugRelTrabajo), 'ko')
    print('\n Régimen turbulento, el factor de fricción es: ', factor_friccion(ReTrabajo,RugRelTrabajo), '\n')
if ReTrabajo > 2300 and ReTrabajo <= 4000 :
    print('\n Zona crítica o de transición, considerando régimen turbulento el factor de fricción es: ', factor_friccion(ReTrabajo,RugRelTrabajo), '\n')
    # SE DECIDE NO MOSTRAR UN PUNTO EN EL GRÁFICO YA QUE NO SERÍA FÍSICAMENTE CORRECTO SUPONER COMPORTAMIENTO TURBULENTO
plt.show()

if ReTrabajo <= 0:
    print('\n Error. Ingrese un Reynolds válido')
    
if RugRelTrabajo < 1e-6 or RugRelTrabajo > 0.1:
    print('\n Error. Ingrese una Rugosidad Relativa válida')
    
curva1=[]
curva2=[]
curva3=[]
ReLista=[]
curva1.append(vectores[4])
curva2.append(vectores[14])
curva3.append(vectores[24])
ReLista.append(Re)
df = ReLista + curva1 + curva2 + curva3
df = pd.DataFrame(df)
df = df.T
df=pd.DataFrame(df.values, columns = ["Re ↓ -  Rugosidad Relativa →", RugRel[4], RugRel[14], np.round(RugRel[24],3)])


pd.DataFrame(df).to_excel("Exportacion.xlsx", header=True, index=False)