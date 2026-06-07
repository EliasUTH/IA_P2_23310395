class AgenteRacionalProbabilista:
    """
    Simula un agente que toma decisiones maximizando su Utilidad Esperada.
    """
    def __init__(self):
        # Diccionario para las probabilidades de los estados del mundo P(S)
        self.creencias_probabilisticas = {}
        # Matriz de utilidades: U(Accion, Estado) -> Recompensa numerica
        self.matriz_utilidad = {}
        self.lista_acciones = set()


    def establecer_creencia(self, estado, probabilidad):
        """Define la probabilidad de que el mundo se encuentre en un estado especifico."""
        self.creencias_probabilisticas[estado] = probabilidad


    def normalizar_creencias(self):
        """Asegura que la suma de todas las probabilidades sea exactamente 1.0"""
        total = sum(self.creencias_probabilisticas.values())
        if total > 0:
            for estado in self.creencias_probabilisticas:
                self.creencias_probabilisticas[estado] /= total


    def establecer_utilidad(self, accion, estado, recompensa):
        """Define la recompensa o costo de tomar una accion bajo un estado especifico."""
        if accion not in self.matriz_utilidad:
            self.matriz_utilidad[accion] = {}
            self.lista_acciones.add(accion)
        self.matriz_utilidad[accion][estado] = recompensa


    def calcular_utilidad_esperada(self, accion):
        """
        Aplica la formula de Utilidad Esperada: 
        UE(A) = Suma( P(S) * U(A, S) ) para todos los estados S.
        """
        utilidad_esperada = 0.0
        

        for estado, probabilidad in self.creencias_probabilisticas.items():
            # Si no hay una utilidad definida, asumimos 0
            recompensa = self.matriz_utilidad.get(accion, {}).get(estado, 0.0)    
            # Valor esperado de esta rama
            valor_rama = probabilidad * recompensa
            utilidad_esperada += valor_rama    
        return utilidad_esperada


    def tomar_decision_racional(self):
        """
        Evalua todas las acciones disponibles y elige la que maximice 
        la utilidad esperada.
        """
        self.normalizar_creencias()
        mejor_accion = None
        maxima_utilidad = float('-inf')
        

        print("Iniciando razonamiento probabilistico...")
        print("Estados del mundo y sus probabilidades:")
        for estado, prob in self.creencias_probabilisticas.items():
            print(f"  - {estado}: {prob * 100:.1f}%")


        print("\nEvaluando acciones:")
        for accion in self.lista_acciones:
            ue_actual = self.calcular_utilidad_esperada(accion)
            print(f"  - Utilidad Esperada de '{accion}': {ue_actual:.2f}")    
            if ue_actual > maxima_utilidad:
                maxima_utilidad = ue_actual
                mejor_accion = accion        
        print("-" * 50)
        print(f"DECISION RACIONAL: El agente decide '{mejor_accion}'")
        print(f"Justificacion: Maximiza la utilidad esperada con un valor de {maxima_utilidad:.2f}")
        print("-" * 50)
        return mejor_accion



# DEMOSTRACION: EL DILEMA DEL AGRICULTOR
if __name__ == "__main__":
    agente = AgenteRacionalProbabilista()
    # 1. Definimos las probabilidades de los estados del clima (Incertidumbre)
    # Segun el pronostico, hay 20% de lluvia abundante, 50% de lluvia normal, 30% de sequia.
    agente.establecer_creencia("lluvia_abundante", 0.20)
    agente.establecer_creencia("lluvia_normal", 0.50)
    agente.establecer_creencia("sequia", 0.30)
    

    # 2. Definimos la matriz de utilidad (Ganancias y Perdidas en miles de dolares)
    # Opcion A: Sembrar Maiz (Requiere mucha agua. Rentable con lluvia, desastroso en sequia)
    agente.establecer_utilidad("sembrar_maiz", "lluvia_abundante", 100)
    agente.establecer_utilidad("sembrar_maiz", "lluvia_normal", 50)
    agente.establecer_utilidad("sembrar_maiz", "sequia", -40)
    

    # Opcion B: Sembrar Sorgo (Resistente a la sequia. Ganancias moderadas pero seguras)
    agente.establecer_utilidad("sembrar_sorgo", "lluvia_abundante", 40)
    agente.establecer_utilidad("sembrar_sorgo", "lluvia_normal", 40)
    agente.establecer_utilidad("sembrar_sorgo", "sequia", 30)
    

    # Opcion C: No hacer nada (Cero riesgo, cero ganancia)
    agente.establecer_utilidad("no_hacer_nada", "lluvia_abundante", 0)
    agente.establecer_utilidad("no_hacer_nada", "lluvia_normal", 0)
    agente.establecer_utilidad("no_hacer_nada", "sequia", 0)
    

    # 3. El agente toma la decision
    print("--- ESCENARIO 1: Pronostico Original ---")
    agente.tomar_decision_racional()
    

    # 4. Cambio en la informacion (Actualizacion de creencias)
    print("\n--- ESCENARIO 2: Llega una alerta de sequia severa ---")
    # Las probabilidades cambian. Ahora la sequia es inminente (80%)
    agente.establecer_creencia("lluvia_abundante", 0.05)
    agente.establecer_creencia("lluvia_normal", 0.15)
    agente.establecer_creencia("sequia", 0.80)
    agente.tomar_decision_racional()