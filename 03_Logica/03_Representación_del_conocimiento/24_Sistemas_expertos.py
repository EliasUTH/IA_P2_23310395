class MotorInferenciaHaciaAtras:
    """
    Motor de inferencia basado en Encadenamiento Hacia Atras (Backward Chaining).
    Trata de probar metas (hipotesis) evaluando sus premisas y, si es necesario,
    consultando al usuario.
    """
    def __init__(self):
        self.base_conocimiento = []
        # Diccionario para almacenar los hechos conocidos y evitar preguntar dos veces
        self.memoria_trabajo = {}
        # Diccionario para traducir variables tecnicas a preguntas legibles
        self.diccionario_preguntas = {}


    def agregar_regla(self, hipotesis, premisas):
        """Agrega una regla a la base de conocimientos."""
        self.base_conocimiento.append({
            "hipotesis": hipotesis,
            "premisas": premisas
        })


    def definir_pregunta(self, variable, texto_pregunta):
        """Asocia una variable logica con una pregunta para el usuario."""
        self.diccionario_preguntas[variable] = texto_pregunta


    def preguntar_al_usuario(self, variable):
        """Interactua con el usuario para obtener evidencia."""
        # Obtenemos el texto de la pregunta, o usamos uno por defecto
        texto = self.diccionario_preguntas.get(variable, f"¿Es cierto el hecho: '{variable}'?")
        print(f"\n[SISTEMA EXPERTO PREGUNTA] {texto}")
        

        # Para que el codigo sea ejecutable de forma automatica en este simulador,
        # usaremos respuestas predefinidas. En un sistema real, se usa 'input()'.
        # respuesta = input("Responda (s/n): ").strip().lower()
        # --- MODO SIMULACION DE USUARIO ---
        respuestas_simuladas = {
            "pc_no_enciende": "n",
            "pc_enciende_pero_no_da_video": "s",
            "emite_pitidos_continuos": "s",
            "pantalla_azul": "n"
        }
        respuesta = respuestas_simuladas.get(variable, "n")
        print(f"[USUARIO RESPONDE] -> {respuesta}")
        es_cierto = (respuesta == 's')
        

        # Guardamos la respuesta en la memoria para no volver a preguntar
        self.memoria_trabajo[variable] = es_cierto
        return es_cierto


    def probar_meta(self, meta, nivel=0):
        """
        Funcion recursiva que intenta probar si una meta (hipotesis o premisa) es cierta.
        """
        sangria = "  " * nivel
        

        # 1. Comprobar si ya conocemos la respuesta (esta en memoria)
        if meta in self.memoria_trabajo:
            return self.memoria_trabajo[meta]


        # 2. Buscar si la meta es la conclusion de alguna regla
        reglas_aplicables = [r for r in self.base_conocimiento if r["hipotesis"] == meta]
        

        # Si no hay reglas que concluyan esto, significa que es un hecho observable.
        # Por lo tanto, debemos preguntarle al usuario.
        if not reglas_aplicables:
            return self.preguntar_al_usuario(meta)
            

        # 3. Si hay reglas, evaluamos sus premisas (Backward Chaining)
        print(f"{sangria}* Analizando hipotesis: '{meta}'...")
        

        for regla in reglas_aplicables:
            print(f"{sangria}  Evaluando regla que requiere: {regla['premisas']}")
            regla_cumplida = True
            

            # Verificamos cada premisa de la regla recursivamente
            for premisa in regla['premisas']:
                if not self.probar_meta(premisa, nivel + 1):
                    regla_cumplida = False
                    break # Si falla una condicion, esta regla fracasa


            # Si todas las premisas de esta regla se cumplen, la meta es cierta
            if regla_cumplida:
                print(f"{sangria}  [✓] Hipotesis confirmada: '{meta}'")
                self.memoria_trabajo[meta] = True
                return True


        # Si ninguna regla aplicable funciono, la meta es falsa
        print(f"{sangria}  [x] Hipotesis descartada: '{meta}'")
        self.memoria_trabajo[meta] = False
        return False

    def diagnosticar(self, lista_posibles_diagnosticos):
        """Inicia el proceso de diagnostico probando una lista de hipotesis principales."""
        print("___SISTEMA EXPERTO DE DIAGNOSTICO DE HARDWARE INICIADO___")
        

        for posible_falla in lista_posibles_diagnosticos:
            # Intentamos probar la falla
            resultado = self.probar_meta(posible_falla)
            

            if resultado:
                print(f"___DIAGNOSTICO FINAL ENCONTRADO___")
                print(f"El problema radica en: {posible_falla.replace('_', ' ').upper()}")
                return
                

        print("___DIAGNOSTICO INCONCLUSO___")
        print("No se pudo determinar el problema con los datos proporcionados.")



# CONFIGURACION DEL SISTEMA EXPERTO
if __name__ == "__main__":
    sistema = MotorInferenciaHaciaAtras()
    # 1. Definir el lenguaje natural de las preguntas (Interfaz de Usuario)
    sistema.definir_pregunta("pc_no_enciende", "¿Al presionar el boton de encendido, la PC no hace absolutamente nada (sin luces ni ventiladores)?")
    sistema.definir_pregunta("cable_poder_conectado", "¿El cable de poder esta correctamente conectado al enchufe?")
    sistema.definir_pregunta("pc_enciende_pero_no_da_video", "¿Los ventiladores giran pero el monitor dice 'Sin Señal'?")
    sistema.definir_pregunta("emite_pitidos_continuos", "¿La tarjeta madre emite pitidos cortos y repetitivos al encender?")
    sistema.definir_pregunta("pantalla_azul", "¿El sistema carga pero de repente muestra una pantalla azul de error?")
    

    # 2. Definir las reglas logicas (Base de Conocimiento)
    # Regla 1: Si no enciende y el cable si esta conectado, falla la fuente de poder.
    sistema.agregar_regla(
        hipotesis="falla_fuente_de_poder",
        premisas=["pc_no_enciende", "cable_poder_conectado"]
    )
    

    # Regla 2: Si enciende sin video y hace pitidos, falla la memoria RAM.
    sistema.agregar_regla(
        hipotesis="falla_memoria_ram",
        premisas=["pc_enciende_pero_no_da_video", "emite_pitidos_continuos"]
    )
    

    # Regla 3: Si enciende sin video y NO hace pitidos, es falla de tarjeta de video.
    # Para simplificar, si sabemos que 'emite_pitidos' es falso, podriamos inferir esto.
    # En este codigo requeriria definir operadores logicos negativos (NOT), asi que usamos reglas afirmativas simples.
    # Regla 4: Pantalla azul es sintoma de falla de sistema operativo.
    sistema.agregar_regla(
        hipotesis="falla_sistema_operativo",
        premisas=["pantalla_azul"]
    )
    

    # 3. Ejecutar el diagnostico
    # Le pasamos al motor las hipotesis globales que debe intentar comprobar
    hipotesis_a_evaluar = [
        "falla_fuente_de_poder", 
        "falla_memoria_ram", 
        "falla_sistema_operativo"
    ]
    sistema.diagnosticar(hipotesis_a_evaluar)