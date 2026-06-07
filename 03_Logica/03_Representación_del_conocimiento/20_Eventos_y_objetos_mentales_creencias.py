import time


class Creencia:
    """Un Objeto Mental. Representa lo que el agente cree que es verdad."""
    def __init__(self, concepto, valor, certeza=1.0):
        self.concepto = concepto
        self.valor = valor
        self.certeza = certeza  # Nivel de seguridad en esta creencia (0.0 a 1.0)


    def __str__(self):
        estado = "V" if self.valor else "F"
        return f"[{self.concepto}: {estado}] (Certeza: {self.certeza*100}%)"


class Evento:
    """Un suceso en el mundo real captado por los sensores."""
    def __init__(self, tipo, datos, fiabilidad_sensor=1.0):
        self.tipo = tipo
        self.datos = datos
        self.fiabilidad = fiabilidad_sensor


class AgenteCognitivo:
    """Un agente de IA que opera basándose en sus Objetos Mentales."""
    def __init__(self, nombre):
        self.nombre = nombre
        self.mente = {}  # Su base de conocimientos interna (Creencias)


    def adoptar_creencia(self, concepto, valor, certeza=1.0):
        self.mente[concepto] = Creencia(concepto, valor, certeza)


    def percibir_evento(self, evento):
        """El agente procesa un evento externo y actualiza sus objetos mentales"""
        print(f"\n[EVENTO SENSORIAL]: El agente '{self.nombre}' ha detectado: {evento.tipo} = {evento.datos}")
        time.sleep(1)


        # Lógica de asimilación del evento
        if evento.tipo in self.mente:
            creencia_actual = self.mente[evento.tipo]


            # Si el sensor es muy fiable y contradice la creencia, el agente cambia de opinión
            if creencia_actual.valor != evento.datos and evento.fiabilidad > 0.5:
                print(f"   [Choque Cognitivo] Mi creencia era {creencia_actual.valor}, pero mis sensores dicen {evento.datos}.")
                print(f"   [Actualización] Modificando mi objeto mental de '{evento.tipo}'...")
                self.mente[evento.tipo].valor = evento.datos
                self.mente[evento.tipo].certeza = evento.fiabilidad
            else:
                print(f"   [Sesgo] Percibí algo distinto, pero confío más en mi creencia actual. Ignorando evento.")
        else:
            # Es un concepto nuevo para el agente
            print(f"   [Nuevo Aprendizaje] No sabía nada sobre '{evento.tipo}'. Adoptando nueva creencia.")
            self.adoptar_creencia(evento.tipo, evento.datos, evento.fiabilidad)



    def razonar_y_actuar(self):
        """El agente decide qué hacer basándose ÚNICAMENTE en sus creencias"""
        print(f"\n[{self.nombre} PENSANDO]:")
        

        # Evalúa su objeto mental sobre la "Lluvia"
        cree_que_llueve = self.mente.get("lluvia")
        if cree_que_llueve and cree_que_llueve.valor is True:
            accion = "Agarra un Paraguas "
        else:
            accion = "Sale con gafas de sol "


        # Evalúa su objeto mental sobre el "Peligro"
        cree_que_hay_peligro = self.mente.get("peligro")
        if cree_que_hay_peligro and cree_que_hay_peligro.valor is True:
            accion += " y camina con mucho cuidado! "
        else:
            accion += " y camina tranquilamente. "
        print(f"   ➔ ACCIÓN DECIDIDA: {accion}")
    def mostrar_mente(self):
        print(f"\n ESTADO MENTAL DE '{self.nombre}':")
        for c in self.mente.values():
            print(f"   - {c}")


# SIMULACIÓN DEL MUNDO Y EL AGENTE

print("___INICIANDO SIMULADOR DE AGENTE COGNITIVO___")


# 1. Creamos al agente
robot = AgenteCognitivo("C3PO")



# 2. Le inyectamos "Falsas Creencias" (Objetos mentales iniciales)
# El robot sale de la fábrica creyendo ciegamente que está lloviendo y no hay peligro.
robot.adoptar_creencia("lluvia", True, certeza=0.9)
robot.adoptar_creencia("peligro", False, certeza=1.0)
robot.mostrar_mente()
time.sleep(1.5)



# 3. El robot actúa basado en su falsa creencia (¡Todavía no ha mirado afuera!)
print("\n--- FASE 1: Acción sin verificar la realidad ---")
robot.razonar_y_actuar()
time.sleep(2)



# 4. Ocurren Eventos en el Mundo Objetivo
print("\n--- FASE 2: Interacción con la Realidad ---")
# El robot abre la puerta, su cámara (sensor) ve un cielo despejado
evento_clima = Evento("lluvia", False, fiabilidad_sensor=0.95)
robot.percibir_evento(evento_clima)



# Su sensor auditivo capta un ladrido fuerte de un perro
evento_sonido = Evento("peligro", True, fiabilidad_sensor=0.8)
robot.percibir_evento(evento_sonido)
time.sleep(1.5)



# 5. El robot re-evalúa su mente y cambia sus acciones
print("\n--- FASE 3: Acción tras actualizar creencias ---")
robot.mostrar_mente()
robot.razonar_y_actuar()