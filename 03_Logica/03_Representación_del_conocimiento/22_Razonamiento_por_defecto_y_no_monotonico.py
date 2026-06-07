class MotorNoMonotonico:
    """
    Motor de inferencia que soporta reglas estrictas y reglas por defecto.
    Permite la retractacion de conclusiones (no monotonicidad) al recalcular
    el estado del mundo desde los hechos base.
    """
    def __init__(self):
        self.hechos_base = set()
        self.reglas_estrictas = []
        self.reglas_defecto = []

    def agregar_hecho_base(self, hecho):
        """Agrega un hecho irrefutable al sistema."""
        self.hechos_base.add(hecho)


    def agregar_regla_estricta(self, condicion, conclusion):
        """Regla logica clasica: Si A es cierto, B siempre es cierto."""
        self.reglas_estrictas.append((condicion, conclusion))


    def agregar_regla_por_defecto(self, condicion, conclusion, excepcion):
        """
        Regla no monotonica: Si A es cierto, asume B, 
        A MENOS QUE se sepa que la excepcion C es cierta.
        """
        self.reglas_defecto.append((condicion, conclusion, excepcion))


    def razonar(self):
        """
        Deriva las conclusiones. Para manejar la no monotonicidad de forma simple,
        reconstruye las inferencias separando el conocimiento estricto del conocimiento asumido.
        """
        hechos_inferidos = set(self.hechos_base)
        

        # PASO 1: Procesar el nucleo monotónico (Reglas Estrictas)
        # Se evaluan primero porque representan verdades absolutas que pueden activar excepciones.
        hubo_cambios = True
        while hubo_cambios:
            hubo_cambios = False
            for condicion, conclusion in self.reglas_estrictas:
                if condicion in hechos_inferidos and conclusion not in hechos_inferidos:
                    hechos_inferidos.add(conclusion)
                    hubo_cambios = True


        # PASO 2: Procesar las asunciones (Reglas por Defecto)
        # Solo se aplican si no entran en conflicto con la excepcion (que pudo ser inferida en el paso 1).
        hubo_cambios = True
        while hubo_cambios:
            hubo_cambios = False
            for condicion, conclusion, excepcion in self.reglas_defecto:
                # Verificamos que se cumpla la condicion y que NO exista la excepcion
                if condicion in hechos_inferidos and excepcion not in hechos_inferidos:
                    if conclusion not in hechos_inferidos:
                        hechos_inferidos.add(conclusion)
                        hubo_cambios = True
                        
        return hechos_inferidos



# DEMOSTRACION DEL SISTEMA
if __name__ == "__main__":
    motor = MotorNoMonotonico()
    # 1. Definicion de Reglas del Mundo
    # Regla estricta: Todo pinguino es un ave.
    motor.agregar_regla_estricta("es_pinguino", "es_ave")
    

    # Regla estricta: Los pinguinos no vuelan (excepcion).
    motor.agregar_regla_estricta("es_pinguino", "no_vuela")
    

    # Regla por defecto: Si es ave, vuela (a menos que sepamos que "no_vuela").
    motor.agregar_regla_por_defecto("es_ave", "vuela", excepcion="no_vuela")
    

    # --- ESCENARIO A: Conocimiento Incompleto ---
    print("--- ESCENARIO A: Vemos a un animal llamado Piolin ---")
    motor.agregar_hecho_base("es_ave") # Solo sabemos que es un ave
    

    estado_mental_A = motor.razonar()
    print("Hechos en la base de datos:")
    for hecho in sorted(estado_mental_A):
        print(f" - {hecho}")


    print("\nAnalisis A: El sistema asume que Piolin 'vuela' por defecto,")
    print("porque no hay evidencia de lo contrario.")
    print("-" * 50)
    

    # --- ESCENARIO B: Llega nueva informacion (No Monotonicidad) ---
    print("\n--- ESCENARIO B: Nos informan que Piolin es de la especie Pinguino ---")
    motor.agregar_hecho_base("es_pinguino") # Agregamos el nuevo hecho
    estado_mental_B = motor.razonar()
    print("Nuevos hechos en la base de datos:")
    for hecho in sorted(estado_mental_B):
        print(f" - {hecho}")  
    print("\nAnalisis B: Observa lo que paso. La conclusion 'vuela' DESAPARECIO.")
    print("Al inferir estrictamente que un pinguino 'no_vuela', la excepcion de la")
    print("regla por defecto se activo, bloqueando la asuncion inicial.")