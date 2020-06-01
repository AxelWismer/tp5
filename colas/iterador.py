import random
from generador_pseudoaliatorio.generador import Generador
from colas.lote import Lote
from colas.salas import SALA_A, SALA_B, SALA_C, SALA_D

class Iteracion:
    def __init__(self, desde=0, hasta=30, ultimas_filas=10, decimales=4):
        self.tabla = []
        self.generador = Generador(decimals=decimales, random=True)
        self.decimales = decimales

        # Inicializacion
        self.numero = 0
        self.evento = 'Inicializacion'
        self.reloj = 0
        self.set_proxima_llegada()

        self.lote_actual = None

        # Resultados
        self.cantidad_visitas = 0
        self.maximo_cola = 0

        # Parametros de visualizacion
        self.desde = desde
        self.hasta = hasta
        self.ultimas_filas = ultimas_filas

    def __str__(self):
        dic = self.as_dict
        dic.pop('salas')
        dic.pop('lotes')
        salas = self.as_dict['salas']
        lotes = self.as_dict['lotes']
        lotes = '\t' + '\n\t'.join([str(lote) for lote in lotes])
        return f"{dic}\n{salas}\n{lotes}\n"

    # Devuelve un diccionario con los valores actuales del objeto
    @property
    def as_dict(self):
        # Creo un diccionario con todos los atributos del objeto
        dic = {
            'numero': self.numero,
            'evento': self.evento,
            'reloj': self.reloj,
            'proxima_llegada': self.proxima_llegada,
            # 'lote_actual': self.lote_actual,
            'cantidad_visitas': self.cantidad_visitas,
            'maximo_cola': self.maximo_cola,
            'salas': {
                'sala_a': SALA_A.as_dict(),
                'sala_b': SALA_B.as_dict(),
                'sala_c': SALA_C.as_dict(),
                'sala_d': SALA_D.as_dict(),
            },
            'lotes': [lote.as_dict() for lote in self.get_lotes()]
        }
        return dic

    def guardar_iteracion(self):
        "Guarda el estado de una iteracion"
        if self.desde <= self.numero <= self.hasta or self.numero > self.numero - self.ultimas_filas:
            self.tabla.append(self.as_dict)

    def set_proxima_llegada(self):
        self.rnd_proxima_llegada = self.generador.exponencial_next(lam=1/5)
        self.proxima_llegada = self.reloj + self.rnd_proxima_llegada
        return self.proxima_llegada

    def get_lotes(self):
        """Obtiene todos los lotes activos en un sistema"""
        return self.get_lotes_en_sala() + self.get_lotes_en_cola()

    def get_lotes_en_sala(self):
        """Devuelve una lista con los lotes en sala de todas las salas"""
        return SALA_A.en_sala + SALA_B.en_sala + SALA_C.en_sala + SALA_D.en_sala

    def get_lotes_en_cola(self):
        """Devuelve una lista con los lotes en sala de todas las colas"""
        return SALA_A.en_cola + SALA_B.en_cola + SALA_C.en_cola + SALA_D.en_cola

    def proximo_lote(self):
        """Devuelve el proximo lote que finalizara el recorrido"""
        lotes = self.get_lotes_en_sala()
        if len(lotes) > 0:
            lote_proximo = lotes[0]
            for lote in lotes[1:]:
                if lote.fin_recorrido < lote_proximo.fin_recorrido:
                    lote_proximo = lote
            return lote_proximo
        return None

    def proximo_evento(self):
        lote_proximo = self.proximo_lote()
        if lote_proximo:
            if self.proxima_llegada < lote_proximo.fin_recorrido:
                self.evento = "llegada"
                self.reloj = self.proxima_llegada
            else:
                self.evento = "fin_recorrido"
                self.lote_actual = lote_proximo
                self.reloj = lote_proximo.fin_recorrido
        self.evento = "llegada"

    # Eventos
    def llegada(self):
        """Setea los campos para el caso de una llegada nueva"""
        # Se agrega el lote a la sala C, se calculan todos los atributos
        # necesarios incluyendo el fin de recorrido si correspondiera
        self.lote_actual = Lote()
        SALA_C.add_lote(self.lote_actual, self.reloj)
        # Se calcula la proxima llegada
        self.set_proxima_llegada()

    def fin_recorrido_sala(self):
        lote = self.lote_actual
        sala = lote.sala_actual

        # Verifica si el lote se encuente en la ultima sala del recorrido
        if lote.ultima_sala():
           # Acciones si un lote llega al final del recorrido
            self.cantidad_visitas += lote.visitantes
            lote.fin_recorrido = None
            # Guardo la iteracion antes de destruir el lote
            self.guardar_iteracion()
            # Elimino el lote anterior
            lote.sala_actual.salir_de_sala(lote)
        # El lote no se encuentra en la ultima sala
        else:
            # Me salgo de la sala actual
            lote.sala_actual.salir_de_sala(lote)
            # Paso a la proxima sala
            lote.proxima_sala()
            # Asigno el lote a la proxima sala
            lote.sala_actual.add_lote(lote, self.reloj)
            self.guardar_iteracion()

        # Se verifica si la sala tenia algun lote en cola y este puede entrar en la sala
        if sala.puede_entrar_a_sala():
            self.entrar_a_sala(sala)

    def entrar_a_sala(self, sala):
        """Se ingresa un objeto desde la cola hasta sus sala calculando su fin de recorrido"""
        # Esta funcion cuenta como una iteracion adicional en caso de que pueda ingresar un lote a la sala
        self.numero += 1
        sala.entrar_a_sala()
        self.guardar_iteracion()

    def calcular_iteracion(self, cant_iteraciones):
        """Metodo que realiza el calculo completo tomando los datos de la iteracion anterior"""
        for i in range(cant_iteraciones):
            self.proximo_evento()
            if self.evento == "llegada":
                self.llegada()
            else:
                self.fin_recorrido_sala()

if __name__ == '__main__':
    it = Iteracion()
    print(it)
    for i in range(10):
        it.calcular_iteracion(1)
        print(it)

