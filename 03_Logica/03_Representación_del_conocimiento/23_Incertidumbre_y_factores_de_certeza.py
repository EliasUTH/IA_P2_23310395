class SistemaExpertoIncertidumbre:
    """
    Motor de inferencia que maneja conocimiento incierto mediante Factores de Certeza (CF).
    Basado en el modelo matematico del sistema experto MYCIN.
    """
    def __init__(self):
        # Diccionario para almacenar los hechos y su nivel de certeza actual (de -1.0 a 1.0)
        self.hechos = {}
        # Lista de reglas: (premisa, hipotesis, factor_certeza_de_la_regla)
        self.reglas = []


    def establecer_hecho(self, hecho, cf):
        """Define o actualiza el Factor de Certeza de un hecho en la base de conocimientos."""
        # Limitamos los valores matematicamente entre -1.0 y 1.0
        cf = max(-1.0, min(1.0, cf))
        self.hechos[hecho] = cf


    def agregar_regla(self, premisa, hipotesis, cf_regla):
        """Agrega una regla heuristica al sistema."""
        self.reglas.append((premisa, hipotesis, cf_regla))


    def combinar_cf(self, cf1, cf2):
        """
        Aplica las formulas matematicas de MYCIN para combinar evidencias independientes
        que apuntan a la misma conclusion.
        """
        # Caso 1: Ambas evidencias son positivas (aumenta la creencia acercandose a 1.0)
        if cf1 > 0 and cf2 > 0:
            return cf1 + cf2 - (cf1 * cf2)


        # Caso 2: Ambas evidencias son negativas (aumenta la descreencia acercandose a -1.0)
        elif cf1 < 0 and cf2 < 0:
            return cf1 + cf2 + (cf1 * cf2)


        # Caso 3: Evidencias conflictivas (una positiva y una negativa)
        else:
            numerador = cf1 + cf2
            denominador = 1 - min(abs(cf1), abs(cf2))
            # Evitar division por cero en caso de conflicto absoluto (-1 y +1)
            if denominador == 0:
                return 0.0
            return numerador / denominador


    def inferir(self):
        """
        Evalua todas las reglas. Si la premisa es creida (CF > 0.2), 
        propaga la certeza hacia la hipotesis.
        """
        print("Iniciando motor de inferencia con incertidumbre...")
        hubo_cambios = True
        umbral_activacion = 0.2 # Solo disparamos reglas si tenemos algo de certeza en la premisa
        

        while hubo_cambios:
            hubo_cambios = False
            for premisa, hipotesis, cf_regla in self.reglas:
                cf_premisa = self.hechos.get(premisa, 0.0)
                

                # Solo procesamos si la premisa tiene suficiente evidencia a favor
                if cf_premisa > umbral_activacion:
                    # Propagacion de la certeza: CF de la evidencia * CF de la regla
                    cf_inferido = cf_premisa * cf_regla
                    cf_actual_hipotesis = self.hechos.get(hipotesis, 0.0)
                    

                    # Si la hipotesis recibe nueva evidencia, calculamos el nuevo CF combinado
                    nuevo_cf_combinado = self.combinar_cf(cf_actual_hipotesis, cf_inferido)
                    

                    # Para evitar bucles infinitos por decimales muy pequeños,
                    # solo actualizamos si el cambio es significativo (mayor a 0.001)
                    if abs(nuevo_cf_combinado - cf_actual_hipotesis) > 0.001:
                        print(f" - Regla aplicada: SI '{premisa}' ENTONCES '{hipotesis}'")
                        print(f"   (CF Premisa: {cf_premisa:.2f} * CF Regla: {cf_regla:.2f} = Evidencia aportada: {cf_inferido:.2f})")
                        print(f"   Actualizando '{hipotesis}': {cf_actual_hipotesis:.2f} -> {nuevo_cf_combinado:.2f}")
                        
                        self.hechos[hipotesis] = nuevo_cf_combinado
                        hubo_cambios = True


    def mostrar_diagnostico(self):
        print("\nEstado Final del Conocimiento (Factores de Certeza):")
        # Ordenamos de mayor certeza a menor certeza
        hechos_ordenados = sorted(self.hechos.items(), key=lambda x: x[1], reverse=True)
        for hecho, cf in hechos_ordenados:
            estado = "Ignorado"
            if cf >= 0.8: estado = "Casi Seguro"
            elif cf >= 0.4: estado = "Probable"
            elif cf >= 0.1: estado = "Leve sospecha"
            elif cf <= -0.8: estado = "Casi Imposible"
            elif cf <= -0.4: estado = "Improbable"
            print(f"[{hecho}]: {cf:+.2f} ({estado})")


# DEMOSTRACION DEL SISTEMA EXPERTO MEDICO
if __name__ == "__main__":
    motor = SistemaExpertoIncertidumbre()
    # 1. Definicion de la Base de Conocimiento (Reglas y su nivel de confianza)
    # Regla 1: Si hay fiebre, hay leve sospecha de infeccion (CF = 0.6)
    motor.agregar_regla("paciente_tiene_fiebre", "posible_infeccion", 0.6)
    

    # Regla 2: Si hay tos severa, hay moderada sospecha de infeccion (CF = 0.7)
    motor.agregar_regla("paciente_tiene_tos", "posible_infeccion", 0.7)
    

    # Regla 3: Si el examen de sangre es normal, disminuye drasticamente la sospecha de infeccion (CF = -0.8)
    motor.agregar_regla("examen_sangre_normal", "posible_infeccion", -0.8)
    

    # 2. Ingreso de hechos observables (Simulando a un paciente real)
    # El termometro marca 38 grados. Estamos 90% seguros de que es fiebre clinica.
    motor.establecer_hecho("paciente_tiene_fiebre", 0.9)
    

    # El paciente tose un poco, pero no estamos tan seguros de que sea tos severa.
    motor.establecer_hecho("paciente_tiene_tos", 0.5)
    

    # El examen de sangre aun no llega, asi que su CF es 0.0 (ignorado).
    print("--- PRIMER DIAGNOSTICO (Basado en sintomas clinicos) ---")
    motor.inferir()
    motor.mostrar_diagnostico()
    

    print("\n" + "="*60 + "\n")
    print("--- SEGUNDO DIAGNOSTICO (Llegan resultados de laboratorio) ---")
    # Los laboratorios confirman que la sangre esta perfectamente normal (Certeza absoluta = 1.0)
    motor.establecer_hecho("examen_sangre_normal", 1.0)
    motor.inferir()
    motor.mostrar_diagnostico()