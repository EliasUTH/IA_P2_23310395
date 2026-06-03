print("=== PROGRAMACIÓN LÓGICA: PARADIGMAS PROLOG Y CLIPS ===\n")
# =====================================================================
# 1. PARADIGMA PROLOG (Orientado a Consultas / Hacia Atrás)
# =====================================================================


class MiniProlog:
    def __init__(self):
        self.hechos = set()
        self.reglas = []


    def assertz(self, hecho):
        """Agrega un hecho a la Base de Conocimiento (Sintaxis Prolog: assertz)."""
        self.hechos.add(hecho)
        print(f"[Prolog] Hecho asertado: {hecho}.")



    def regla(self, cabeza, cuerpo_func):
        """
        Define una regla. En Prolog real sería: cabeza :- cuerpo.
        Aquí usamos una función lambda o estándar para evaluar el cuerpo.
        """
        self.reglas.append((cabeza, cuerpo_func))
        print(f"[Prolog] Regla definida para: {cabeza}.")


    def query(self, objetivo):
        """Ejecuta una consulta (Goal) usando encadenamiento hacia atrás simplificado."""
        print(f"\n?- {objetivo}.") # Formato clásico de consulta en consola Prolog
        

        # 1. ¿Es un hecho directo?
        if objetivo in self.hechos:
            print("   True.")
            return True
            

        # 2. ¿Puede deducirse por una regla?
        for cabeza, cuerpo in self.reglas:
            if cabeza == objetivo:
                if cuerpo(self): # Pasamos la instancia para que evalúe recursivamente
                    print("   True.")
                    return True
                    
        print("   False.")
        return False



# =====================================================================
# 2. PARADIGMA CLIPS (Orientado a Producción / Hacia Adelante)
# =====================================================================
class MiniCLIPS:
    def __init__(self):
        self.working_memory = set() # Memoria de Trabajo (Hechos dinámicos)
        self.rule_base = []         # Base de Reglas (Producciones)


    def assert_fact(self, hecho):
        """Inyecta datos en la Memoria de Trabajo (Sintaxis CLIPS: assert)."""
        if hecho not in self.working_memory:
            self.working_memory.add(hecho)
            print(f"[CLIPS] ==> (assert {hecho})")


    def defrule(self, nombre, condicion_func, accion_func):
        """Define una regla de producción (Sintaxis CLIPS: defrule)."""
        self.rule_base.append({"nombre": nombre, "if": condicion_func, "then": accion_func, "disparada": False})
        print(f"[CLIPS] Regla compilada: {nombre}")


    def run(self):
        """Motor de Inferencia. Ciclo de Reconocimiento-Acción."""
        print("\n[CLIPS] (run)")
        cambios = True
        ciclo = 1
        

        # El motor corre hasta que ninguna regla nueva pueda dispararse
        while cambios:
            cambios = False
            agenda = []
            # Fase 1: Reconocimiento (Match) - Ver qué reglas cumplen sus condiciones
            for regla in self.rule_base:
                if not regla["disparada"] and regla["if"](self.working_memory):
                    agenda.append(regla) 
            # Fase 2: Resolución de Conflictos y Acción (Fire)
            for regla in agenda:
                print(f"   [FIRE] Disparando regla: {regla['nombre']}")
                regla["then"](self) # Ejecuta la acción (suele ser hacer nuevos asserts)
                regla["disparada"] = True
                cambios = True
            ciclo += 1
        print("[CLIPS] Halt. No hay más reglas en la agenda.\n")



# =====================================================================
# 3. EJECUCIÓN Y COMPARACIÓN DE LOS PARADIGMAS
# =====================================================================
print("--- ESCENARIO A: SISTEMA EXPERTO CON PROLOG ---")
# Problema: Determinar si un animal es un ave.
prolog = MiniProlog()


# Declaraciones puras
prolog.assertz("tiene_plumas(piolin)")
prolog.assertz("vuela(piolin)")
prolog.assertz("tiene_pelo(firulais)")


# Regla: Es ave SI tiene plumas Y vuela.
prolog.regla("es_ave(piolin)", lambda p: p.query("tiene_plumas(piolin)") and p.query("vuela(piolin)"))


# Ejecutamos consultas
prolog.query("es_ave(piolin)")
prolog.query("es_ave(firulais)")
print("\n" + "-"*60 + "\n")


print("--- ESCENARIO B: SISTEMA DE CONTROL CON CLIPS ---")
# Problema: Control automático de un reactor nuclear.
clips = MiniCLIPS()


# Hechos iniciales de los sensores
clips.assert_fact("(temperatura_alta)")
clips.assert_fact("(valvula_cerrada)")


# Reglas de Producción
clips.defrule(
    nombre="alerta_presion",
    condicion_func=lambda wm: "(temperatura_alta)" in wm and "(valvula_cerrada)" in wm,
    accion_func=lambda engine: engine.assert_fact("(presion_peligrosa)")
)


clips.defrule(
    nombre="activar_refrigeracion",
    condicion_func=lambda wm: "(presion_peligrosa)" in wm,
    accion_func=lambda engine: engine.assert_fact("(refrigeracion_ON)")
)


# Arrancamos el motor continuo
clips.run()
print("Memoria de trabajo final de CLIPS:")
for f in clips.working_memory:
    print(f" - {f}")


print("\n=== ANÁLISIS TÉCNICO ===")
print("1. El Enfoque Prolog (Top-Down): Partes de tu objetivo ('es_ave') y excavas hacia abajo para encontrar las pruebas. No gastas CPU comprobando si 'firulais' es un ave hasta que el usuario lo pregunte.")
print("2. El Enfoque CLIPS (Bottom-Up): No hay un 'objetivo' explícito. El sistema reacciona a los datos del entorno ('temperatura_alta') y deduce hacia arriba ('refrigeracion_ON') automáticamente. Es un sistema reactivo.")
print("3. Integración Real: En la industria real, no construyes estos motores desde cero. Utilizas librerías de Python como 'pySWIP' (para conectar con un motor de SWI-Prolog real) o 'clipspy' (para enlazar con el motor C de CLIPS).")