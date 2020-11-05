from matplotlib.pylab import *
from matplotlib import cm


# Definiciones geometricas
a = 1.     #alto del dominio
b = 1.     #ancho del dominio

Nx = 30    #numero de intervalos en X
Ny = 30    #numero de intervalos en Y

dx = b/Nx  #discretizacion espacial en x
dy = a/Ny  #discretizacion espacial en y


if dx != dy:
    print("Error dx != dy")
    exit(-1)

h = dx

#Funciones de conveniencia para calcular las coordenadas del punto(1,j)

def coords(i,j):
    return (dx*1, dy*j)

x,y= coords(4,2)

print("x: ",x)
print("y: ",y)

def imshowbien(u):
    imshow(u.T[Nx::-1,:],cmap=cm.coolwarm, interpolation='bilinear')
    cbar = colorbar(extend='both', cmap=cm.coolwarm)
    ticks = arange(0,35,5)
    ticks_Text=["{}°".format(deg) for deg in ticks]
    cbar.set_ticks(ticks)
    cbar.set_ticklabels(ticks_Text)
    clim(0, 30)
    
    xlabel('b')
    ylabel('a')
    xTicks_N = arange(0, Nx+1, 3)
    yTicks_N = arange(0, Ny+1, 3)
    xTicks =[coords(i,0)[0] for i in xTicks_N]
    yTicks =[coords(0,i)[0] for i in yTicks_N]
    xTicks_Text = ["{0:.2f}".format(tick) for tick in xTicks]
    yTicks_Text = ["{0:.2f}".format(tick) for tick in yTicks]
    xticks(xTicks_N,xTicks_Text, rotation='vertical')
    yticks(yTicks_N,yTicks_Text)
    margins(0,2)
    subplots_adjust(bottom=0.15)
    
    
u_k = zeros((Nx+1,Ny+1),dtype=double)
u_km1 = zeros((Nx+1,Ny+1),dtype=double)

#Condicion de borde inicial
u_k[:,:] = 5. #5 grados inicial en todas partes

#Parametros del problema (hierro)
dt = 0.01   #s
K = 79.5
c = 450.    #
rho = 7800.
alpha = K*dt/(c*rho*dx**2)

#informar cosas interesantes
print(f"dt = {dt}")
print(f"dx = {dx}")
print(f"K = {K}")
print(f"c = {c}")
print(f"rho = {rho}")
print(f"alpha = {alpha}")

#Loop en el tiempo
minuto = 60.
hora = 3600.
dia = 24 * 3600

dt = 1*minuto
dnext_t = 0.5*hora

next_t = 0
framenum = 0

T = 1*dia
Days = 1*T #Cuantos dias quiero simular

#Vectores para acumular la t° en Puntos Interesantes
p_1=zeros(int32(Days/dt))     
p_2=zeros(int32(Days/dt))  
p_3=zeros(int32(Days/dt)) 

def truncate(n, decimals=0):
    multiplier = 10 ** decimals
    return int(n * multiplier) / multiplier

#Loop en el tiempo K
for k in range(int32(Days/dt)):
    t = dt*(k+1)
    dias = truncate(t/dia,0)
    horas = truncate((t-dias*dia)/hora,0)
    minutos = truncate((t-dias*dia-horas*hora)/minuto,0)
    titulo = "k = {0:05.0f}".format(k) + " t = {0:02.0f}d {1:02.0f}h {2:02.0f}m ".format(dias, horas, minutos)
    print(titulo)
    
    
    #CB esenciales, se repiten en cada iteración
    u_k[0,:] = 25.   #Borde izquierdo
    u_k[:,0] = u_k[:,-1]-0*dy   #Borde inferior gradiente 0
    u_k[:,-1] = u_k[:,-2]-0*dy #Borde superior gradiente 0
    u_k[-1,:] = 25 #Borde derecho 
    
    #Escribiendo Puntos Interesantes
    p_1[k]=u_k[int(Nx/2),int(Ny/2)]     #medio,medio
    p_2[k]=u_k[int(Nx/2),int(3*Ny/4)]   #medio,3/4
    p_3[k]=u_k[int(3*Nx/4),int(3*Ny/4)] #3/4,3/4
    
    #Loop en el espacio i = 1 ...... n-1
    for i in range(1,Nx):
        for j in range(1,Ny):
            #Algoritmo de diferencia finitas 2-D para difusión
            nabla_u_k = (u_k[i-1, j] + u_k[i+1,j] + u_k[i, j-1] + u_k[i, j+1] - 4*u_k[i,j]) / h**2
            
            #Forward Euler
            u_km1[i,j] = u_k[i,j] + alpha*nabla_u_k
    
    #Avanzar la solución a k+1
    u_k = u_km1
    
    #CB denuevo, para asegurar cumpliemiento
    u_k[0,:] = 25.   #Borde izquierdo
    u_k[:,0] = u_k[:,-1]-0*dy   #Borde inferior gradiente 0
    u_k[:,-1] = u_k[:,-2]-0*dy #Borde superior gradiente 0
    u_k[-1,:] = 25 #Borde derecho 
    
    if t > next_t:
        figure(1)
        imshowbien(u_k)
        title(titulo)
        savefig("caso_5/frame_{0:04.0f}.png".format(framenum))
        framenum += 1
        next_t += dnext_t
        close(1)
        
#Ploteo historia de t° en Puntos Interesantes 
figure(2)
plot(range(int32(Days/dt)),p_1,label='N/2,N/2')
plot(range(int32(Days/dt)),p_2,label='N/2,3N/4')
plot(range(int32(Days/dt)),p_3,label='3N/4,3N/4')

title("Evolución de temperatura en puntos")
legend()
savefig(f'caso_5.png')
show()      
        
        