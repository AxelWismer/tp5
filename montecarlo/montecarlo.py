import random

randoms = [0.94, 0.74, 0.62, 0.11, 0.17, 0.66, 0.54, 0.30, 0.69, 0.08,
           0.27, 0.13, 0.80, 0.10, 0.54, 0.60, 0.49, 0.78, 0.66, 0.44]


class Producto:
    def __init__(self, c, p, tr, cr, si, num_pseudoaleatorios=[]):
        self.costo = c
        self.precio_venta = p
        self.tiempo_reposicion = tr
        self.cant_a_reponer = cr
        self.stock_inicial = si
        self.demanda = 0
        self.disponibilidad = 0
        self.stock = 0
        self.reposicion = False
        self.cant_vendida = 0
        self.ingreso = 0
        self.costo_reposicion = 0
        self.beneficio_total = 0
        self.tabla = []
        self.iteracion = {}
        self.dia = 0

        # Array de numeros pseudoaleatorios
        # Si no se ingresa uno el programa trabajara con el random del sistema
        self.numeros_pseudoaleatorios  = num_pseudoaleatorios
        self.cont_numeros_pseudoaleatorios = 0

    # Devuelve el proximo numero aleatorio
    def next_rnd(self):
        # Si la posicion se sale del rango del array (o el array estaba vacio)
        # Genera los proximos numeros con el random del lenguaje
        if self.cont_numeros_pseudoaleatorios >= len(self.numeros_pseudoaleatorios):
            rnd = random.random()
        else:
            # Si no devuelve el proximo valor del array
            rnd = self.numeros_pseudoaleatorios[self.cont_numeros_pseudoaleatorios]
            self.cont_numeros_pseudoaleatorios += 1
        return rnd

    def set_demanda(self):
        rnd = self.next_rnd()
        # Agregar al diccionario
        self.iteracion['rnd'] = round(rnd, 4)
        if rnd < 0.15:
            self.demanda = 3
        elif rnd < 0.4:
            self.demanda = 4
        elif rnd < 0.75:
            self.demanda = 5
        elif rnd < 0.95:
            self.demanda = 6
        else:
            self.demanda = 7

    def set_reposicion(self, dia):
        if dia == 1:
            self.reposicion = True
        elif (dia % self.tiempo_reposicion) == 1:
            self.reposicion = True
        else:
            self.reposicion = False

    def set_disponibilidad(self, dia):
        if self.reposicion:
            self.disponibilidad = self.stock + 15
        else:
            self.disponibilidad = self.stock

    def set_stock(self):
        if (self.disponibilidad - self.demanda) < 0:
            self.stock = 0
        else:
            self.stock = self.disponibilidad - self.demanda

    def set_cant_vendida(self):
        self.cant_vendida = self.disponibilidad - self.stock

    def set_ingreso(self):
        self.ingreso = self.precio_venta * self.cant_vendida

    def set_costo_reposicion(self):
        if self.reposicion:
            self.costo_reposicion = self.costo * self.cant_a_reponer
        else:
            self.costo_reposicion = 0

    def set_total(self):
        total = self.ingreso - self.costo_reposicion
        self.iteracion['total'] = total
        self.beneficio_total = self.beneficio_total + total

    def guardar_iteracion(self):
        self.iteracion['dia'] = self.dia
        self.iteracion['demanda'] = self.demanda
        self.iteracion['reposicion'] = self.reposicion
        self.iteracion['disponible'] = self.disponibilidad
        self.iteracion['stock'] = self.stock
        self.iteracion['venta'] = self.cant_vendida
        self.iteracion['ingreso'] = self.ingreso
        self.iteracion['costo'] = self.costo_reposicion
        self.iteracion['total_acum'] = self.beneficio_total

        iteracion = self.iteracion
        self.iteracion = {}
        return iteracion

    def simular(self, cant_iteraciones):
        for i in range(cant_iteraciones):
            self.dia += 1
            self.set_demanda()
            self.set_reposicion(i+1)
            self.set_disponibilidad(i+1)
            self.set_stock()
            self.set_cant_vendida()
            self.set_ingreso()
            self.set_costo_reposicion()
            self.set_total()

            self.tabla.append(self.guardar_iteracion())
            # Guardar datos de la iteracion
            self.guardar_iteracion()
        # print(self.tabla)
        return self.beneficio_total


class ProductoSinVencimiento(Producto):
    def __init__(self, c, p, tr, cr, si, r, num_pseudoaleatorios=[]):
        super(ProductoSinVencimiento, self).__init__(c, p, tr, cr, si, num_pseudoaleatorios)
        self.recupero = r

    def set_recupero(self):
        self.beneficio_total += self.stock * self.recupero

    def simular(self, cant_iteraciones):
        super(ProductoSinVencimiento, self).simular(cant_iteraciones)
        self.set_recupero()

        self.tabla[-1]['total_acum'] = self.beneficio_total

        return self.beneficio_total

class ProductoConVencimiento(Producto):

    def __init__(self, c, p, tr, cr, si, v, num_pseudoaleatorios=[]):
        Producto.__init__(self, c, p, tr, cr, si, num_pseudoaleatorios)
        self.vencimiento = v

    def set_disponibilidad(self, dia):
        if (dia % self.vencimiento) == 1:
            # se desecha lo vencido
            self.disponibilidad = 0
            if self.reposicion:
                self.disponibilidad = 15
        else:
            if self.reposicion:
                self.disponibilidad = self.stock + 15
            else:
                self.disponibilidad = self.stock


if __name__ == '__main__':
    producto1 = ProductoConVencimiento(10, 16, 3, 15, 15, 3)
    producto2 = Producto(13, 16, 3, 15, 15, num_pseudoaleatorios=randoms)
    print(producto1.simular(15))
    print(producto2.simular(15))
