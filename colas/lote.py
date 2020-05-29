from generador_pseudoaliatorio.generador import Generador
from colas.salas import SALA_A, SALA_B, SALA_C, SALA_D

generador = Generador(decimals=4, random=True)

class Lote:
    nro = 0
    instances = set()

    @classmethod
    def get_nro(cls):
        """Devuelve para cada nuevo objeto un valor unico"""
        cls.nro += 1
        return cls.nro

    # @classmethod
    # def fin_recorrido_proximo(cls):
    #     lotes = cls.
    #
    # @classmethod
    # def get_instances(cls):
    #     dead = set()
    #     for ref in cls.instances:
    #         obj = ref()
    #         if obj is not None:
    #             yield obj
    #         else:
    #             dead.add(ref)
    #     cls.instances -= dead

    def __init__(self):
        self.numero = Lote.get_nro()
        self.sala_actual = None
        self.cola = False
        self.visitantes = generador.poisson_next(3)
        self.recorrido = self.get_recorrido(generador.rnd())
        self.fin_recorrido = ''

    def __str__(self):
        return str(self.as_dict()) + '\n'

    @property
    def estado(self):
        sala = self.sala_actual
        if sala:
            return f'En sala {sala.nombre}' if not self.cola else f'En sala {sala.nombre}'
        return ""

    def recorrido_as_str(self):
        return [sala.nombre for sala in self.recorrido]

    def as_dict(self):
        return {
            'numero': self.numero,
            'estado': self.estado,
            'visitantes': self.visitantes,
            'recorrido': self.recorrido_as_str(),
            'fin_recorrido': self.fin_recorrido,
        }

    def set_fin_recorrido(self, reloj):
        self.fin_recorrido = reloj + self.sala_actual.tiempo_recorrido

    def get_recorrido(self, rnd):
        """Calcula el recorrido de un grupo"""
        if rnd < 0.6:
            return [SALA_C, SALA_D]
        elif rnd < 0.8:
            return [SALA_C, SALA_A, SALA_B, SALA_D]
        else:
            return [SALA_C, SALA_A, SALA_D]

    def ultima_sala(self):
        return self.sala_actual == self.recorrido[-1]

    def proxima_sala(self):
        if not self.ultima_sala():
            self.sala_actual = self.recorrido[self.recorrido.index(self.sala_actual) + 1]
        else:
            raise Exception("No existe proxima sala")

if __name__ == '__main__':
    x = 0
    # # Pruebas
    # print(SALA_A)
    # lote = Lote()
    # print(lote.as_dict())
    # # Agregar lote
    # SALA_A.add_lote(lote)
    # print(SALA_A)
    # # Eliminar lote
    # SALA_A.salir_de_sala(lote)
    # print(SALA_A)

    # Agregar lotes hasta que entren en cola
    # lotes = (Lote() for x in range(20))
    # for lote in lotes:
    #     SALA_A.add_lote(lote)
    #     print(lote)
    #     print(SALA_A)
    #     print()
    # for lote in SALA_A.en_sala: print(lote, end='')
    # print()
    # for lote in SALA_A.en_cola: print(lote, end='')

    # Siguiente sala de un lote
    # lote = Lote()
    # SALA_C.add_lote(lote, 5)
    # print(SALA_C)
    # # Lote en primera sala
    # print(lote)
    # lote.proxima_sala()
    # # Lote en segunda sala
    # print(lote)


    # Ultima sala
    # lote = Lote()
    # SALA_C.add_lote(lote)
    # print(SALA_C)
    # lote.recorrido = [SALA_D, SALA_C]
    # # Lote en primera sala
    # print(lote)
    # lote.proxima_sala() #Debe producir un error
    # # Lote en segunda sala
    # print(lote)

    # Probar incrementar el numero de una sala
    a = Lote()
    b = Lote()
    print(list(Lote.get_instances()))
    b = 0
    print(list(Lote.get_instances()))