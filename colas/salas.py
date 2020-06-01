# Salas (servidores)
from generador_pseudoaliatorio.generador import Generador

class Sala:

    def __init__(self, nombre, capacidad, decimales=4):
        self.nombre = nombre
        self.capacidad_inicial = capacidad
        self.generador = Generador(decimals=decimales, random=True)
        self.en_sala = []
        self.en_cola = []

    def __str__(self):
        return str(self.as_dict)

    @property
    def tiempo_recorrido(self):
        pass

    def as_dict(self):
        return {
            'nombre': self.nombre,
            "col": self.cola,
            "capacidad": self.capacidad,
        }

    @property
    def capacidad(self):
        capacidad_ocupada = sum(lote.visitantes for lote in self.en_sala)
        return self.capacidad_inicial - capacidad_ocupada

    @property
    def cola(self):
        return sum(lote.visitantes for lote in self.en_cola)

    def hay_espacio(self, visitantes):
        """Verifica si un nuevo lote puede ingresar a la sala"""
        return visitantes <= self.capacidad

    def add_lote(self, lote, reloj):
        "Agrega un nuevo lote, ya sea a la sala o a la cola"
        lote.sala_actual = self
        if self.hay_espacio(lote.visitantes) and self.cola==0:
            lote.cola = False
            self.en_sala.append(lote)
            # Como el lote entra a la sala se calcula su fin de recorrido utilizando el tiempo actual
            lote.set_fin_recorrido(reloj)
        else:
            lote.cola = True
            self.en_cola.append(lote)

    def puede_entrar_a_sala(self):
        return self.hay_espacio(self.en_cola[0].visitantes)

    def entrar_a_sala(self):
        """Mueve un lote de la cola a la sala"""
        if self.puede_entrar_a_sala():
            lote = self.en_cola.pop(0)
            self.add_lote(lote)

    def salir_de_sala(self, lote):
        """Saca un lote de la sala"""
        self.en_sala.remove(lote)


class SalaNormal(Sala):
    def __init__(self, nombre, capacidad, media, desviacion, decimales=4):
        super(SalaNormal, self).__init__(nombre, capacidad, decimales)
        self.media = media
        self.desviacion = desviacion

    @property
    def tiempo_recorrido(self):
        return self.generador.box_muller_next(media=self.media, desviacion=self.desviacion)


class SalaUniforme(Sala):
    def __init__(self, nombre, capacidad, minimo, maximo, decimales=4):
        super(SalaUniforme, self).__init__(nombre, capacidad, decimales)
        self.minimo = minimo
        self.maximo = maximo

    @property
    def tiempo_recorrido(self):
        return self.generador.uniforme_next(a=self.minimo, b=self.maximo)


SALA_A = SalaNormal("A", capacidad=40, media=30, desviacion=5)
SALA_B = SalaNormal("B", capacidad=40, media=25, desviacion=4)
SALA_C = SalaUniforme("C", capacidad=100, minimo=12, maximo=18)
SALA_D = SalaUniforme("D", capacidad=100, minimo=14, maximo=18)

if __name__ == '__main__':
    print(SALA_A, SALA_B, SALA_C, SALA_D)
