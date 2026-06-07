class RazonamientoDeductivo:
    """
    Simula un motor de inferencia clásico. 
    Se le proporciona la regla universal desde el principio (programacion tradicional)
    y este la aplica para clasificar nuevos casos.
    """
    def __init__(self, regla_universal):
        self.regla = regla_universal


    def deducir(self, instancia):
        for i in range(len(self.regla)):
            # Si la regla exige un valor especifico y la instancia no lo tiene, falla
            if self.regla[i] != '?' and self.regla[i] != instancia[i]:
                return False
        return True



class AprendizajeInductivo:
    """
    Simula un agente de Machine Learning usando el algoritmo Find-S.
    NO tiene reglas preprogramadas. Descubre la regla general a partir de los datos.
    """
    def __init__(self):
        # La hipotesis comienza vacia
        self.hipotesis = None



    def entrenar(self, ejemplos_positivos):
        """
        Proceso de Induccion: Observa casos especificos para crear una regla general.
        """
        print("Iniciando proceso de induccion (Algoritmo Find-S)...")
        


        # 1. Tomamos el primer ejemplo como nuestra hipotesis inicial mas especifica
        self.hipotesis = list(ejemplos_positivos[0])
        print(f" - Hipotesis inicial (basada en ejemplo 1): {self.hipotesis}")



        # 2. Iteramos sobre los demas ejemplos para generalizar
        for num, ejemplo in enumerate(ejemplos_positivos[1:], start=2):
            for i in range(len(self.hipotesis)):
                # Si el atributo del ejemplo nuevo contradice nuestra hipotesis actual,
                # significa que ese atributo no es determinante. Lo generalizamos con '?' (Cualquiera).
                if self.hipotesis[i] != '?' and self.hipotesis[i] != ejemplo[i]:
                    self.hipotesis[i] = '?'          
            print(f" - Hipotesis tras observar ejemplo {num}: {self.hipotesis}")
        print("Aprendizaje completado.")
        return self.hipotesis



    def predecir(self, nueva_instancia):
        """Usa la regla inducida para evaluar un nuevo caso."""
        if not self.hipotesis:
            return "Modelo no entrenado."
        for i in range(len(self.hipotesis)):
            if self.hipotesis[i] != '?' and self.hipotesis[i] != nueva_instancia[i]:
                return False # No cumple con el patron aprendido
        return True



# DEMOSTRACION: EL PROBLEMA DE JUGAR TENIS
if __name__ == "__main__":
    # Cada instancia tiene 4 atributos: [Clima, Temperatura, Humedad, Viento]
    # PARTE 1: EL ENFOQUE TRADICIONAL (RAZONAMIENTO DEDUCTIVO)
    print("___ENFOQUE 1: RAZONAMIENTO DEDUCTIVO (Experto Humano)___")

    


    # Un humano programa la regla general directamente: 
    # "Solo se juega si esta Soleado y el Viento es Debil, sin importar temperatura o humedad"
    regla_humana = ['Soleado', '?', '?', 'Debil']
    motor_deductivo = RazonamientoDeductivo(regla_humana)
    dia_hoy = ['Soleado', 'Frio', 'Alta', 'Debil']
    decision = motor_deductivo.deducir(dia_hoy)
    print(f"Regla programada: {regla_humana}")
    print(f"Evaluando el dia: {dia_hoy}")
    print(f"Conclusion deductiva: {'Se juega' if decision else 'No se juega'}")


    # PARTE 2: EL ENFOQUE DE IA (APRENDIZAJE INDUCTIVO)
    print("\n___ENFOQUE 2: APRENDIZAJE INDUCTIVO (Descubrimiento)___")
    # El sistema no conoce ninguna regla. Solo se le dan datos historicos
    # de dias donde SI se jugo al tenis (Ejemplos positivos).
    base_de_datos = [
        ['Soleado', 'Caluroso', 'Normal', 'Fuerte'], # Dia 1 (Se jugo)
        ['Soleado', 'Templado', 'Normal', 'Fuerte'], # Dia 2 (Se jugo)
        ['Soleado', 'Frio', 'Alta', 'Fuerte']        # Dia 3 (Se jugo)
    ]
    


    print("Datos historicos proporcionados:")
    for i, dato in enumerate(base_de_datos, 1):
        print(f" Dia {i}: {dato}")
    print("")
    motor_inductivo = AprendizajeInductivo()
    


    # El agente procesa los datos de lo especifico a lo general
    regla_aprendida = motor_inductivo.entrenar(base_de_datos)
    print(f"\nREGLA GENERAL INDUCIDA POR LA IA: {regla_aprendida}")
    print("Traduccion: La IA descubrio que el patron comun es que siempre esta 'Soleado' y el viento es 'Fuerte'.")
    print("La Temperatura y la Humedad cambiaban, asi que las descarto como irrelevantes (?).")



    # Prueba del modelo inducido
    print("\n--- Poniendo a prueba lo aprendido ---")
    nuevo_dia_1 = ['Soleado', 'Caluroso', 'Alta', 'Fuerte']
    nuevo_dia_2 = ['Lluvioso', 'Frio', 'Normal', 'Fuerte']
    print(f"¿Se juega en {nuevo_dia_1}? -> {'Si' if motor_inductivo.predecir(nuevo_dia_1) else 'No'}")
    print(f"¿Se juega en {nuevo_dia_2}? -> {'Si' if motor_inductivo.predecir(nuevo_dia_2) else 'No'}")