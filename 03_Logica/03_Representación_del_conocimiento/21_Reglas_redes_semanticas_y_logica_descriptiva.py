# 1. REDES SEMANTICAS
class RedSemantica:
    """
    Representa el conocimiento mediante un grafo dirigido.
    """
    def __init__(self):
        self.grafo = {}


    def agregar_nodo(self, sujeto, relacion, objeto):
        if sujeto not in self.grafo:
            self.grafo[sujeto] = []
        self.grafo[sujeto].append((relacion, objeto))


    def consultar(self, sujeto):
        if sujeto in self.grafo:
            resultados = []
            for relacion, objeto in self.grafo[sujeto]:
                resultados.append(f"{sujeto} --[{relacion}]--> {objeto}")
            return resultados
        return ["No se encontro informacion en la red semantica."]


# 2. LOGICA DESCRIPTIVA (TBox y ABox)
class LogicaDescriptiva:
    """
    Representa el conocimiento mediante una separacion estricta 
    entre terminologia (conceptos) y aserciones (individuos).
    """
    def __init__(self):
        # TBox (Terminological Box): Guarda jerarquias (Subsumcion)
        self.tbox = {} 
        # ABox (Assertional Box): Asigna individuos a conceptos
        self.abox = {}


    def definir_concepto(self, subconcepto, superconcepto):
        """Construye la TBox definiendo que un concepto esta subsumido por otro."""
        self.tbox[subconcepto] = superconcepto


    def afirmar_individuo(self, individuo, concepto):
        """Construye la ABox declarando la existencia de un individuo en un concepto."""
        self.abox[individuo] = concepto


    def deducir_pertenencia(self, individuo, concepto_buscado):
        """
        Razonador basico: Evalua si un individuo pertenece a un concepto superior
        rastreando la jerarquia en la TBox.
        """
        if individuo not in self.abox:
            return False
        concepto_actual = self.abox[individuo]
        # Bucle para escalar en la jerarquia de conceptos
        while concepto_actual is not None:
            if concepto_actual == concepto_buscado:
                return True
            # Subimos un nivel en la jerarquia (si no hay mas, devuelve None)
            concepto_actual = self.tbox.get(concepto_actual)
        return False


# 3. SISTEMA BASADO EN REGLAS
class MotorReglas:
    """
    Motor de inferencia hacia adelante (Forward Chaining).
    Deriva nuevo conocimiento aplicando reglas a los hechos existentes.
    """
    def __init__(self):
        self.hechos = set()
        self.reglas = []


    def agregar_hecho(self, hecho):
        self.hechos.add(hecho)


    def agregar_regla(self, condiciones, conclusion):
        # 'condiciones' es una lista de strings. 'conclusion' es un string.
        self.reglas.append((condiciones, conclusion))


    def inferir(self):
        """Ejecuta las reglas hasta que no se puedan deducir mas hechos."""
        hubo_cambios = True
        iteracion = 1
        print("Iniciando motor de inferencia...") 
        while hubo_cambios:
            hubo_cambios = False
            for condiciones, conclusion in self.reglas:
                # Comprobamos si TODAS las condiciones de la regla estan en nuestra base de hechos
                # y verificamos que la conclusion no se haya inferido antes
                if all(condicion in self.hechos for condicion in condiciones) and conclusion not in self.hechos:
                    print(f" - Iteracion {iteracion}: Se cumplio {condiciones}.")
                    print(f"   -> Nuevo hecho inferido: {conclusion}")
                    self.hechos.add(conclusion)
                    hubo_cambios = True
            iteracion += 1           
        print("Inferencia completada.")



# EJECUCION Y DEMOSTRACION
if __name__ == "__main__":
    print("--- DEMOSTRACION DE REDES SEMANTICAS ---")
    red = RedSemantica()
    red.agregar_nodo("Pajaro", "TIENE", "Alas")
    red.agregar_nodo("Pajaro", "PUEDE", "Volar")
    red.agregar_nodo("Pinguino", "ES_UN", "Pajaro")
    red.agregar_nodo("Pinguino", "NO_PUEDE", "Volar")
    

    for relacion in red.consultar("Pinguino"):
        print(relacion)
    for relacion in red.consultar("Pajaro"):
        print(relacion)


    print("\n--- DEMOSTRACION DE LOGICA DESCRIPTIVA ---")
    ld = LogicaDescriptiva()
    

    # 1. Alimentamos la TBox (Definicion del mundo)
    ld.definir_concepto("Perro", "Mamifero")
    ld.definir_concepto("Mamifero", "Vertebrado")
    ld.definir_concepto("Vertebrado", "Animal")
    

    # 2. Alimentamos la ABox (Hechos del mundo real)
    ld.afirmar_individuo("Firulais", "Perro")
    

    # 3. Consulta al razonador
    objetivo = "Animal"
    resultado = ld.deducir_pertenencia("Firulais", objetivo)
    print(f"Pregunta: ¿Es 'Firulais' un '{objetivo}'?")
    print(f"Respuesta logica: {'Verdadero' if resultado else 'Falso'}")


    print("\n--- DEMOSTRACION DE SISTEMA DE REGLAS ---")
    motor = MotorReglas()
    

    # Estado inicial del mundo
    motor.agregar_hecho("alerta_sismica_activada")
    motor.agregar_hecho("en_edificio")
    


    # Base de conocimiento (Reglas de negocio/supervivencia)
    motor.agregar_regla(["alerta_sismica_activada"], "emergencia_confirmada")
    motor.agregar_regla(["emergencia_confirmada", "en_edificio"], "iniciar_evacuacion")
    motor.agregar_regla(["iniciar_evacuacion"], "dirigirse_a_punto_de_encuentro")
    


    # Ejecutar el motor
    motor.inferir()
    print("\nBase de hechos finales almacenada en el sistema:")
    for hecho in sorted(motor.hechos):
        print(f" - {hecho}")