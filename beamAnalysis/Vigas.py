#Programa para cálculo de vigas bi apoiada

import numpy as np
import math
from matplotlib import pyplot as plt

l = 6 #m
q = 200 #kN/m
q1 = 5 #kN/m --> Carga triangular no início da viga
q2 = 10 #kN/m --> Carga triangular no final da viga
p = 5000 #kN --> Carga concentrada
xp = 4.5 #kN --> Coordenada [m] da carga concentrada a partir do início da viga
b = 0.2 #m
h = 0.4 #m
E = 30000000 #kN/m²
I = b * pow(h,3) / 12


n = 100 #Fator de escala para o gráfico (100 = cm)
x = np.linspace (0,l,num = n*l+1)

def CargaDistribuida (q,l):
    Va = q*l/2
    Vb = Va
    momento = (Va * x) - (q*pow(x,2)/2)
    cortante = Va - q*x
    deslocamento = q * x * (pow(l,3) - 2 * l * pow(x,2) + pow(x,3)) / (24 * E * I)
    result = [momento,cortante, deslocamento]
    return result

def CargaPontual (p,xp,l): 
    a = xp
    b = l-xp
        
    momento = []
    cortante = []
    deslocamento = []
    i = 0
    for element in x:
        
        if x[i] <= a:
            momento.append(p*b*x[i]/l)
            cortante.append(p*b/l)
            deslocamento.append(p * b * x[i] * (pow(l, 2) - pow(b, 2) - pow(x[i], 2)) / (6 * E * I * l))
        else:
            momento.append(p*b*x[i]/l -p*(x[i]-a))
            cortante.append(-p*a/l)
            deslocamento.append(p * a * (b - (x[i] - a)) * (pow(l, 2) - pow(a, 2) - pow(b - (x[i] - a), 2)) / (6 * E * I * l))
        i = i+1
    result = [momento,cortante, deslocamento]
    
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
        #deslocamento = 
    else: #Condição de carga crescente
        xres1 = l-l/3
        momento = q*l*x/6 - q*pow(x,3)/(6*l)
        cortante = q*l/6 - q*pow(x,2)/(2*l)
        #deslocamento = 
        
    parcelaRetangular = CargaDistribuida(qmin,l)
    
    result = [momento+parcelaRetangular[0],cortante+parcelaRetangular[1]]    
       
    return result

momento = CargaDistribuida(q,l) [0] + CargaTriangular(q1,q2,l) [0] + CargaPontual(p,xp,l)[0]
cortante = CargaDistribuida(q,l) [1] + CargaTriangular(q1,q2,l) [1] + CargaPontual(p,xp,l)[1]
# !!!CargaTriangular faltando!!!
deslocamento = (CargaDistribuida(q,l) [2] + CargaPontual(p,xp,l)[2]) * 100
mmax = np.max(momento)
mmin = np.min(momento)
vmax = np.max(abs(cortante))
vmin = np.min(abs(cortante))
dmax = np.max(deslocamento)
dmin = np.min(deslocamento)

print("Momento máximo: " + str(mmax))
print("Momento mínimo: " + str(mmin))
print("Cortante máximo: " + str(vmax))
print("Cortante mínimo: " + str(vmin))
print("Deslocamento máximo: " + str(dmax))
print("Deslocamento mínimo: " + str(dmin))


def CordMaxMin (momento, cortante, deslocamento, mmax,mmin,vmax,vmin, dmax, dmin):
    i = 0
    
    xMax = []
    for item in x:
        if mmax == momento[i]:
            xMmax = x[i]
        if mmin == momento [i]:
            xMmin = x[i]
        if vmax == abs(cortante [i]):
            xVmax = x[i]
        if vmin == abs(cortante[i]):
            xVmin = x[i]
        if dmax == deslocamento[i]:
            xDmax = x[i]            
        if dmin == deslocamento[i]:
            xDmin = x[i]
        i = i +1
    
    result = [xMmax,xMmin,xVmax,xVmin, xDmax, xDmin] 

    return result

extremos = CordMaxMin(momento, cortante, deslocamento, mmax, mmin, vmax, vmin, dmax, dmin)
print(extremos)

plt.figure (figsize=(15,10))
plt.subplot(3, 1, 1)
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




plt.subplot(3, 1, 2)
plt.title("Diagrama de Esforço Cortante", fontsize=20, color='blue', loc='left')
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


plt.subplot(3, 1, 3)
plt.title("Deslocamento", fontsize=20, color='blue', loc='left')
plt.plot ([0]*len(x), color="k")
plt.fill (-deslocamento, alpha=0.1)
plt.plot (-deslocamento, color="darkBlue")
plt.vlines(extremos[4]*n,0,-dmax, color = "red")
plt.annotate('Dmax = '+ str(np.round(dmax,2)) + "cm" + "\n x = " + str(np.round(extremos[4],2)) + "m", xy=(extremos[4]*n, -dmax), xytext=(extremos[4]*n+5, -dmax+dmax/2),
            arrowprops=None, rotation=90, color = "red")

j = 0
for i in x:
  if float.is_integer(i):
    k = j
    if i > 0 and i < l:
      plt.annotate('D= ' + str(np.round(deslocamento[k],0)) +  "cm", xy=(x[k]*n, -dmax/2), xytext=(x[k]*n+5, -dmax/2),arrowprops=None, rotation=90)
      plt.vlines(x[k]*n, 0,-deslocamento[k], color = "lightBlue")   
  j = j+1



# plt.annotate('X= ' + str(np.round(extremos[3],2)) +  "m", xy=(extremos[3]*10, vmin), xytext=(extremos[3]*10, vmin +4),
#            arrowprops=None)
#plt.annotate('V= '+ str(np.round(cortante[0],1)) + "kN", xy=(1,1), xytext=(0.5,cortante[0]-cortante[0]/1.1),
#            arrowprops=None, rotation=90)
#plt.annotate('V= '+ str(np.round(cortante[len(cortante)-1],1)) + "kN", xy=(1,1), xytext=(x[len(x)-1]*10+0.5,cortante[len(cortante)-1]-cortante[len(cortante)-1]/2),
#            arrowprops=None, rotation=90)

plt.show()