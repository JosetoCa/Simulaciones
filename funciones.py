import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageFont

class planos:
    """
    Clase para representar objetos planos cuadrados en un montaje óptico y su propagación
    """
    def __init__(self, N=1024, wl=0.532e-3, tamaño_mm=10):
        """
        Parámetros:
        N : int
            Tamaño, en píxeles, de los planos.
        wl : float
            Longitud de onda del montaje (en milímetros)
        tamaño_mm : float
            Tamaño físico total del plano (en milímetros)
        """
        self.N = N
        self.wl = wl
        self.tamaño_mm = tamaño_mm
        self.dx = tamaño_mm / N  # resolución espacial (mm/píxel)

    def centro_cuadrado(self, l):
        """
        Ventana cuadrada centrada de lado l mm. Amplitud 1.

        l : float
            Ancho de la ventana en mm
        
        Return:
            plano : ndarray ventana
        """
        l_pix = int(round(l * self.N / self.tamaño_mm)) # lado en píxeles

        if l_pix > self.N:
            raise ValueError("La ventana es más grande que el plano.")
        
        plano = np.zeros((self.N, self.N))
        i0 = int((self.N - l_pix) / 2)
        i1 = int((self.N + l_pix) / 2)
        plano[i0:i1, i0:i1] = 1
        return plano

    def iris(self, radio):
        """
        Iris centrado.

        radio : float
            radio del iris en mm
        
        Return:
            iris : ndarray
        """

        radio_pix = int(round(radio * self.N / self.tamaño_mm))
        if radio_pix > self.N:
            raise ValueError("El iris es más grande que el plano.")
        centro = self.N // 2
        x = np.arange(self.N)
        y = np.arange(self.N)
        X, Y = np.meshgrid(x, y)

        distancia_cuadrada = (X - centro)**2 + (Y - centro)**2
        iris = np.zeros((self.N, self.N))
        iris[distancia_cuadrada <= radio_pix**2] = 1
        return iris
    
    def lente_delgado_centrado(self, f):
        """
        Fase de lente delgada (ap. paraxial), sin término constante.

        f : float
            Foco en milímetros.
        
        Return:
            lente : ndarray máscara de fase dada por la lente
        """

        x = np.linspace(-self.tamaño_mm/2, self.tamaño_mm/2, self.N)
        X, Y = np.meshgrid(x, x)
        lente = np.exp(-1j * np.pi * (X**2 + Y**2) / (self.wl * f))
        return lente
    def mostrar_campo(self, u2, título="Campo propagado"):
        plt.figure(figsize=(15, 4))

        # Intensidad
        plt.subplot(1, 3, 1)
        plt.imshow(np.abs(u2)**2, cmap='gray',
               extent=[-self.tamaño_mm/2, self.tamaño_mm/2,
                       -self.tamaño_mm/2, self.tamaño_mm/2])
        plt.title("Intensidad")
        plt.colorbar()

        # Amplitud
        plt.subplot(1, 3, 2)
        plt.imshow(np.abs(u2), cmap='gray',
               extent=[-self.tamaño_mm/2, self.tamaño_mm/2,
                       -self.tamaño_mm/2, self.tamaño_mm/2])
        plt.title("Amplitud")
        plt.colorbar()

        # Fase
        plt.subplot(1, 3, 3)
        plt.imshow(np.angle(u2), cmap='twilight',
               extent=[-self.tamaño_mm/2, self.tamaño_mm/2,
                       -self.tamaño_mm/2, self.tamaño_mm/2])
        plt.title("Fase")
        plt.colorbar()

        plt.suptitle(título)
        plt.tight_layout()
        plt.show()
    def asignar_objeto(self, nombre, matriz):
        """
        Asigna una estructura personalizada como parte del plano.

        nombre : str
            Nombre del objeto
        matriz : ndarray
            Campo a guardar
        """
        if not hasattr(self, "objetos"):
            self.objetos = {}
        self.objetos[nombre] = matriz
    def letra(self, letra: str, tamaño_fuente: int):
        """
        Genera un plano con una letra en fuente Free sans.
        Es importante verificar que se puede acceder a la fuente

        letra : str
            Letra en la imagen
        tamaño fuente : ndarray
            Altura, en píxeles, de la letra.
            
        Return:
            matriz : ndarray con la imagen de la letra.
        """
        
        img = Image.new('L', (self.N,self.N), color = 0)
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype("C:\Proyectos\Simulaciones\FreeSans-LrmZ.ttf", size = tamaño_fuente)
        draw.text((256,0), letra, fill = 255, font=font)
        matriz = np.array(img)/255
        return matriz

    
class propagacion:
    """
    Clase para simular la propación de los campos de objetos planos cuadrados en el montaje óptico.
    """
    def __init__(self, tamaño_mm=10, N = 1024, wl = 0.532e-3):
        """
        Parámetros
        ----------
        tamaño_mm : float
            Ancho del plano, en mm. Por defecto 10.0 mm 
        N : int
            Tamaño de la matriz del plano. Por defecto 1024
        wl : float
            Longitud de onda en mm. Por defecto  0.532e-3 mm (verde).
        """
        self.tamaño_mm = tamaño_mm
        self.N = N
        self.wl = wl
        self.dx = tamaño_mm / N  # resolución espacial (mm/píxel)

    def propaTF(self, u1, z):
        """
        Propagación libre del campo en ap. parxial con la función de transferencia

         Parámetros:
            u1 : ndarray
                Campo complejo en el plano z = 0 (entrada).
            z : float
                Distancia de propagación en milímetros.

        Return:
             u2 : ndarray
                Campo propagado a distancia z.
        """
        k = 2*np.pi/self.wl
        fx = np.fft.fftfreq(self.N, d=self.dx) 
        FX, FY = np.meshgrid(fx, fx)
        H = np.exp(1j*k*z)*np.exp(-1j*np.pi*self.wl*z*(FX**2+FY**2))
        U1 = np.fft.fft2(u1)
        
        u2 = np.fft.ifft2(U1*H)

        return u2
    
    

