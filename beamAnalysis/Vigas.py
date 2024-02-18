#Programa para cálculo de vigas bi apoiada
#A unidade kN é ruim! Vamos substituir para kgf ou tf.

import numpy as np
import math
from matplotlib import pyplot as plt

l = 5 #m
q = 200 #kN/m
q1 = 5 #kN/m --> Carga triangular no início da viga
q2 = 10 #kN/m --> Carga triangular no final da viga
p = 500 #kN --> Carga concentrada
xp = 4.5 #kN --> Coordenada [m] da carga concentrada a partir do início da viga

n = 100 #Fator de escala para o gráfico (100 = cm)
x = np.linspace (0,l,num = n*l+1)

def CargaDistribuida (q,l):
    Va = q*l/2
    Vb = Va
    momento = (Va * x) - (q*pow(x,2)/2)
    cortante = Va - q*x
    result = [momento,cortante]
    return result

def CargaPontual (p,xp,l): 
    a = xp
    b = l-xp
        
    momento = []
    cortante = []
    i = 0
    for element in x:
        
        if x[i] <= a:
            momento.append(p*b*x[i]/l)
            cortante.append(p*b/l)
        else:
            momento.append(p*b*x[i]/l -p*(x[i]-a))
            cortante.append(-p*a/l)
        
        i = i+1
    result = [momento,cortante]
    
    return result

def CargaTriangular (q1,q2,l): #Em elaboração
    qmax = max(q1,q2)
    qmin = min(q1,q2)
    qres = l*(qmax-qmin)/2
    q = qmax-qmin
    
    if qmax == q1: #Condição de carga decrescente
        xres1 = l/3
        momento = q*l*x/6 - q*pow(x,3)/(6*l)
        cortante = q*l/6 + q*pow(x,2)/(2*l)
    else: #Condição de carga crescente
        xres1 = l-l/3
        momento = q*l*x/6 - q*pow(x,3)/(6*l)
        cortante = q*l/6 - q*pow(x,2)/(2*l)
        
    parcelaRetangular = CargaDistribuida(qmin,l)
    
    result = [momento+parcelaRetangular[0],cortante+parcelaRetangular[1]]    
       
    return result

momento = CargaDistribuida(q,l) [0] + CargaTriangular(q1,q2,l) [0] + CargaPontual(p,xp,l)[0]
cortante = CargaDistribuida(q,l) [1] + CargaTriangular(q1,q2,l) [1] + CargaPontual(p,xp,l)[1]
mmax = np.max(momento)
mmin = np.min(momento)
vmax = np.max(abs(cortante))
vmin = np.min(abs(cortante))

print("Momento máximo: " + str(mmax))
print("Momento mínimo: " + str(mmin))
print("Cortante máximo: " + str(vmax))
print("Cortante mínimo: " + str(vmin))


def CordMaxMin (momento, cortante,mmax,mmin,vmax,vmin):
    i = 0
    
    for item in x:
        if mmax == momento[i]:
            xMmax = x[i]
        if mmin == momento [i]:
            xMmin = x[i]
        if vmax == abs(cortante [i]):
            xVmax = x[i]
        if vmin == abs(cortante[i]):
            xVmin = x[i]
        i = i +1
    
    result = [xMmax,xMmin,xVmax,xVmin] 
    
    return result

extremos = CordMaxMin(momento, cortante,mmax,mmin,vmax,vmin)

plt.figure (figsize=(15,10))
plt.subplot(2, 1, 1)
plt.title("Diagrama de Momento Fletor", fontsize=20, color='blue', loc='left')
plt.plot ([0]*len(x), color="k")
plt.fill (-momento, alpha=0.1)
plt.plot (-momento, color="darkBlue")
plt.vlines(extremos[0]*n,0,-mmax, color = "red")
plt.annotate('Mmax = '+ str(np.round(mmax,1)) + "kNm" + "\n x = " + str(np.round(extremos[0],2)) + "m", xy=(extremos[0]*n, -mmax), xytext=(extremos[0]*n+5, -mmax+mmax/2),
            arrowprops=None, rotation=90, color = "red")

j = 0
for i in x:
  if float.is_integer(i):
    k = j
    if i > 0 and i < l:
      plt.annotate('M= ' + str(np.round(momento[k],0)) +  "kNm", xy=(x[k]*n, -mmax/2), xytext=(x[k]*n+5, -mmax/2),arrowprops=None, rotation=90)
      plt.vlines(x[k]*n, 0,-momento[k], color = "lightBlue")   
  j = j+1




plt.subplot(2, 1, 2)
plt.plot ([0]*len(x), color="k")
plt.plot (cortante, color="darkBlue")

j = 0
for i in x:
  if float.is_integer(i):
    k = j  
    if cortante[k] > 0:
      plt.annotate('V= ' + str(np.round(cortante[k],0)) +  "kN", xy=(x[k]*n, -10), xytext=(x[k]*n, -vmax/2),arrowprops=None, rotation=90)
      plt.vlines(x[k]*n, 0,cortante[k], color = "lightblue")
    if cortante[k] <0:
      plt.annotate('V= ' + str(np.round(cortante[k],0)) +  "kN", xy=(x[k]*n, +10), xytext=(x[k]*n, cortante[0]/3),arrowprops=None, rotation=90)
      plt.vlines(x[k]*n, 0,cortante[k], color = "lightblue")      
  j = j+1

plt.vlines(x[0],0,cortante[0], color="darkBlue")
plt.vlines(x[len(x)-1]*n, 0,cortante[len(x)-1], color = "darkBlue")
plt.title("Diagrama de Esforço Cortante", fontsize=20, color='blue', loc='left')
# plt.annotate('X= ' + str(np.round(extremos[3],2)) +  "m", xy=(extremos[3]*10, vmin), xytext=(extremos[3]*10, vmin +4),
#            arrowprops=None)
#plt.annotate('V= '+ str(np.round(cortante[0],1)) + "kN", xy=(1,1), xytext=(0.5,cortante[0]-cortante[0]/1.1),
#            arrowprops=None, rotation=90)
#plt.annotate('V= '+ str(np.round(cortante[len(cortante)-1],1)) + "kN", xy=(1,1), xytext=(x[len(x)-1]*10+0.5,cortante[len(cortante)-1]-cortante[len(cortante)-1]/2),
#            arrowprops=None, rotation=90)

plt.show()
