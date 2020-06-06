import random

from generador_pseudoaliatorio.generador import Generador
from colas.lote import Lote
from colas.salas import SALA_A, SALA_B, SALA_C, SALA_D

class Iteracion:
    def __init__(self, desde=0, hasta=30, ultimas_filas=10, decimales=4):
        self.tabla = []
        self.tabla_final = [None] * ultimas_filas
        self.pos_ultimo_elemento = 0
        self.generador = Generador(decimals=decimales, random=True)
        self.decimales = decimales
        self.cantidad_iteraciones = 1

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
        lotes = '\t' + '\n\t'.join([lote for lote in lotes])
        return f"{dic}\n{salas}\n{lotes}\n"

    def print_tabla(self, tabla):
        print("Tabla")
        for linea in tabla:
            dic = linea.copy()
            salas = dic.pop('salas')
            lotes = dic.pop('lotes')
            lotes = '\t' + '\n\t'.join([str(lote) for lote in lotes.items()])
            print(f"{dic}\n{salas}\n{lotes}")
            print("-" * 20)

    # Devuelve un diccionario con los valores actuales del objeto
    @property
    def as_dict(self):
        # Creo un diccionario con todos los atributos del objeto
        dic = {
            'numero': self.numero,
            'evento': self.evento,
            'reloj': round(self.reloj, self.decimales),
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
            'lotes': {lote.numero : lote.as_dict() for lote in self.get_lotes()}
        }
        return dic

    def guardar_iteracion(self):
        "Guarda el estado de una iteracion"
        if self.desde <= self.numero <= self.hasta:
            self.tabla.append(self.as_dict)
        else:
            self.tabla_final[self.pos_ultimo_elemento] = self.as_dict
            # Actualizo el proximo elemnto a reemplazar cuidando de que se mantenga en el rango de las ultimas filas
            self.pos_ultimo_elemento = int((self.pos_ultimo_elemento + 1) % self.ultimas_filas)

    def ordenar_tabla_final(self):
        "Ordena la tabla final"
        self.tabla_final = self.tabla_final[self.pos_ultimo_elemento:] + self.tabla_final[:self.pos_ultimo_elemento]

    def set_proxima_llegada(self):
        self.rnd_proxima_llegada = self.generador.exponencial_next(lam=1/5)
        self.proxima_llegada = round(self.reloj + self.rnd_proxima_llegada, self.decimales)
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
        else:
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
        else:
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
        acu = 0
        for i in range(len(SALA_C.en_cola)):
            acu += SALA_C.en_cola[i].visitantes
        if acu > self.maximo_cola:
            self.maximo_cola = acu
        self.guardar_iteracion()

    def fin_recorrido_sala(self):
        lote = self.lote_actual
        sala = lote.sala_actual

        lote_en_cola = None

        # Verifica si el lote se encuente en la ultima sala del recorrido
        if lote.ultima_sala():
           # Acciones si un lote llega al final del recorrido
            self.cantidad_visitas += lote.visitantes
            lote.fin_recorrido = None
            # Actualizo la cantidad total de visitas
            self.cantidad_visitas += lote.visitantes

            # Se verifica si la sala tenia algun lote en cola y este puede entrar en la sala
            for i in range(len(sala.en_cola)):
                if sala.puede_entrar_a_sala_desde_cola():
                    lote_en_cola = sala.en_cola[0]
                    self.entrar_a_sala_desde_cola(sala, lote_en_cola)
                    sala.en_cola.pop(0)
                    # Guardo la iteracion despues de haber cambiado al lote a su nueva sala

            # Guarda la iteracion con todos los cambios realizados
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

            # Se verifica si la sala tenia algun lote en cola y este puede entrar en la sala
            for i in range(len(sala.en_cola)):
                if sala.puede_entrar_a_sala_desde_cola():
                    lote_en_cola = sala.en_cola[0]
                    self.entrar_a_sala_desde_cola(sala, lote_en_cola)
                    sala.en_cola.pop(0)
                    # Guardo la iteracion despues de haber cambiado al lote a su nueva sala
                # Guarda la iteracion con todos los cambios realizados
            self.guardar_iteracion()

    def entrar_a_sala_desde_cola(self, sala, lote):
        """Se ingresa un objeto desde la cola hasta sus sala calculando su fin de recorrido"""
        # Esta funcion cuenta como una iteracion adicional en caso de que pueda ingresar un lote a la sala
        # No se si corresponde sumar una iteracion
        sala.en_sala.append(lote)
        lote.cola = False
        lote.set_fin_recorrido(self.reloj)

    def calcular_iteracion(self, tiempo):
        """Metodo que realiza el calculo completo tomando los datos de la iteracion anterior"""
        while self.reloj < tiempo:
            self.numero += 1
            self.proximo_evento()
            if self.evento == "llegada":
                self.llegada()
            else:
                self.fin_recorrido_sala()

    # Mostrar los lotes de un intervalo en una matriz
    def get_matrix(self, tabla):
        lotes = set()
        # Obtengo los numeros de todos los lotes en todas las iteraciones y elimino los duplicados
        for linea in tabla:
            lotes.update(list(linea["lotes"].keys()))

        lotes = list(lotes)
        # Creo una matriz llena de diccionarios vacios
        # matriz = [[None] * numero_columnas] * numero_filas
        # {'numero': '', 'estado': '', 'visitantes': '', 'recorrido': '' , 'fin_recorrido': ''}
        matriz = [[{'numero': '', 'estado': '', 'visitantes': '', 'recorrido': '' , 'fin_recorrido': ''}] * len(lotes) for i in range(len(tabla))]

        for i in range(len(tabla)):
            linea = tabla[i]
            # print(i, list)
            for j in range(len(lotes)):
                numero = lotes[j]
                # print("Lineas:", list(linea['lotes'].keys()))
                # print("Numeros:", numero)
                # print("en: ", numero in list(linea['lotes'].keys()))
                # Si el lote existe en esta linea
                if numero in list(linea['lotes'].keys()):
                    matriz[i][j] = linea['lotes'][numero]
                    # print(linea['lotes'][numero])

        # Agrego los lotes a la tabla
        for i in range(len(tabla)):
            tabla[i]['lotes_arreglados'] = matriz[i]

        return tabla, lotes

        # Ver tabla
        # for i in range(len(tabla)):
        #     for j in range(len(lotes)):
        #         print(matriz[i][j], end="\n\t")
        #     print()
        #     print("-" * 20)
        #
        # Ver que matrices se registraron en cada fila
        # for i in range(len(tabla)):
        #     for j in range(len(lotes)):
        #         print(matriz[i][j]["numero"], end=" | ")
        #     print()
        #     print("-" * 20)


    def limpiar_salas(self):
        """Limpia todas las salas para una nueva simulacion"""
        SALA_A.limpiar_sala()
        SALA_B.limpiar_sala()
        SALA_C.limpiar_sala()
        SALA_D.limpiar_sala()
        Lote.resetrar_lote()


if __name__ == '__main__':
    it = Iteracion(desde=0, hasta=30)
    print(it)
    it.reloj = it.proxima_llegada
    it.calcular_iteracion(1000)
    it.print_tabla(it.tabla)
    # it.print_tabla(it.tabla_final)
    print(len(it.tabla))
    it.get_matrix(tabla=it.tabla)
