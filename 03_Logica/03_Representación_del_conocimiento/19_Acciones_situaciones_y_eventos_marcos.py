class Marco:
    """Clase base para el motor de representación por Marcos"""
    def __init__(self, nombre, padre=None):
        self.nombre = nombre
        self.padre = padre       # Para permitir herencia
        self.ranuras = {}        # Slots del marco



    def agregar_ranura(self, nombre, valor=None, default=None, if_needed=None, if_added=None):
        """Define una nueva ranura (slot) con sus respectivas facetas (facets)"""
        self.ranuras[nombre] = {
            'valor': valor,
            'default': default,
            'if_needed': if_needed,  # Demonio de lectura
            'if_added': if_added     # Demonio de escritura (Disparador)
        }



    def obtener(self, nombre_ranura):
        """Consulta el valor de una ranura evaluando las facetas lógicas"""
        ranura = self.ranuras.get(nombre_ranura)
        


        # 1. Si la ranura no existe aquí, buscar en el marco padre (Herencia)
        if not ranura:
            if self.padre:
                return self.padre.obtener(nombre_ranura)
            return f"No existe la ranura '{nombre_ranura}'."



        # 2. Si tiene un valor explícito, lo retornamos
        if ranura['valor'] is not None:
            return ranura['valor']



        # 3. FACETA: if_needed (Si no hay valor, calcularlo en el momento)
        if ranura['if_needed']:
            print(f"   [Demonio if_needed] Calculando valor para '{nombre_ranura}' al vuelo...")
            return ranura['if_needed'](self)




        # 4. FACETA: default (Si no hay nada más, dar el valor por defecto)
        if ranura['default'] is not None:
            return ranura['default']
        return "Vacío"




    def asignar(self, nombre_ranura, nuevo_valor):
        """Asigna un valor a una ranura y dispara eventos si es necesario"""
        if nombre_ranura not in self.ranuras:
            # Si no existe, creamos una ranura básica sin facetas especiales
            self.agregar_ranura(nombre_ranura)

        self.ranuras[nombre_ranura]['valor'] = nuevo_valor
        # FACETA: if_added (Disparar reacción en cadena al modificar)
        demon_if_added = self.ranuras[nombre_ranura].get('if_added')
        if demon_if_added:
            demon_if_added(self, nuevo_valor)


# CONSTRUYENDO NUESTRO MUNDO Y SUS REGLAS
print("___INICIANDO MOTOR DE MARCOS (FRAMES)___")




# --- 1. MARCO SITUACIONAL (Entidades y Estados) ---
# Creamos el concepto abstracto de "Persona"
marco_persona = Marco("Concepto_Persona")
marco_persona.agregar_ranura("especie", default="Humano")
marco_persona.agregar_ranura("estado_animo", default="Tranquilo")
marco_persona.agregar_ranura("energia", default=100)



# Creamos una instancia específica que hereda de Persona
juan = Marco("Juan", padre=marco_persona)
print("1 ESTADO INICIAL DE JUAN:")
print(f" - Energía: {juan.obtener('energia')}")
print(f" - Estado de ánimo: {juan.obtener('estado_animo')}")



# --- 2. DEFINIENDO LOS DEMONIOS (Lógica de los Eventos) ---
def calcular_cansancio(marco_actor):
    """Demonio if_needed: Calcula dinámicamente si alguien necesita descansar"""
    energia = marco_actor.obtener("energia")
    return "Sí, necesita dormir" if energia < 50 else "No, está fresco"



def ejecutar_accion_correr(marco_evento, actor):
    """Demonio if_added: La acción altera la situación del actor"""
    print(f"\n   [Demonio if_added activado]: Se detectó la acción de Correr.")
    print(f"   Consecuencias aplicándose a '{actor.nombre}'...")
    energia_actual = actor.obtener("energia")
    # La acción reduce la energía y cambia el estado de ánimo
    actor.asignar("energia", energia_actual - 60)
    actor.asignar("estado_animo", "Agotado y Sudoroso")


# Añadimos la ranura que calcula el cansancio al vuelo usando if_needed
juan.agregar_ranura("necesita_descanso", if_needed=calcular_cansancio)



# --- 3. MARCO DE ACCIÓN / EVENTO ---
# Definimos el estereotipo de la acción "Correr un Maratón"
accion_correr = Marco("Evento_Correr_Maraton")
accion_correr.agregar_ranura("lugar", default="Pista de Atletismo")
accion_correr.agregar_ranura("dificultad", default="Alta")
# Aquí conectamos el demonio de escritura: Si alguien se asigna como "actor" de esta acción, se dispara el evento
accion_correr.agregar_ranura("actor", if_added=ejecutar_accion_correr)


# SIMULACIÓN DEL MUNDO
print("\n2 CONSULTANDO ANTES DE LA ACCIÓN:")
print(f" - ¿Juan necesita descanso?: {juan.obtener('necesita_descanso')}")


print("3 ¡OCURRE UN EVENTO! Asignando a Juan a la Acción 'Correr'...")
# En el momento en que guardamos a 'juan' en la ranura 'actor', el demonio if_added despierta
accion_correr.asignar("actor", juan)
print("\nESTADO FINAL (SITUACIÓN ALTERADA):")
print(f" - Nueva Energía: {juan.obtener('energia')}")
print(f" - Nuevo Estado: {juan.obtener('estado_animo')}")
print(f" - ¿Juan necesita descanso?: {juan.obtener('necesita_descanso')}")