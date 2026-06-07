class ReglaDominio:
    """Representa el conocimiento previo que tiene la maquina sobre el mundo."""
    def __init__(self, conclusion, premisas):
        self.conclusion = conclusion
        self.premisas = premisas


class AprendizajePorExplicacion:
    """
    Motor de Aprendizaje EBL.
    Construye una explicacion para un ejemplo y extrae la informacion relevante
    para crear una nueva regla generalizada.
    """
    def __init__(self, teoria_dominio):
        self.teoria_dominio = teoria_dominio


    def construir_explicacion(self, meta, hechos_observados, nivel=0):
        """
        Intenta demostrar la meta usando encadenamiento hacia atras.
        Si tiene exito, devuelve la lista de los hechos base estrictamente necesarios.
        """
        sangria = "  " * nivel
        

        # 1. Caso Base: La meta es directamente un hecho observable (Informacion Relevante)
        if meta in hechos_observados:
            print(f"{sangria} [Hecho Base] '{meta}' confirmado por observacion.")
            return True, [meta]
            

        # 2. Paso Deductivo: Buscar reglas que concluyan la meta
        reglas_aplicables = [r for r in self.teoria_dominio if r.conclusion == meta]
        

        for regla in reglas_aplicables:
            print(f"{sangria} Intentando explicar '{meta}' mediante premisas: {regla.premisas}")
            explicacion_exitosa = True
            hechos_relevantes_acumulados = []
            

            # Evaluar cada premisa de la regla recursivamente
            for premisa in regla.premisas:
                exito, hechos_necesarios = self.construir_explicacion(premisa, hechos_observados, nivel + 1)
                if exito:
                    hechos_relevantes_acumulados.extend(hechos_necesarios)
                else:
                    explicacion_exitosa = False
                    print(f"{sangria}   Fallo al explicar '{premisa}'. Regla descartada.")
                    break


            if explicacion_exitosa:
                print(f"{sangria} [✓] '{meta}' explicado exitosamente.")
                return True, hechos_relevantes_acumulados


        # Si ninguna regla puede explicarlo, fracasa
        return False, []


    def aprender_regla_general(self, concepto_objetivo, ejemplo_entrenamiento):
        """
        Proceso central de EBL: Explica, aisla lo relevante y generaliza.
        """
        print(f"\nIniciando Aprendizaje EBL para el concepto: '{concepto_objetivo}'")
        print(f"Observando el siguiente ejemplo de entrenamiento: {ejemplo_entrenamiento}")
        print("-" * 50)
        

        # Fase 1: Explicacion (Identificar por que es un ejemplo positivo)
        exito, informacion_relevante = self.construir_explicacion(concepto_objetivo, ejemplo_entrenamiento)
        print("-" * 50)
        if exito:
            # Eliminar duplicados manteniendo el orden
            info_relevante_unica = list(dict.fromkeys(informacion_relevante))
            

            # Fase 2: Generalizacion (Ignorar lo irrelevante y crear macro-operador)
            info_irrelevante = [hecho for hecho in ejemplo_entrenamiento if hecho not in info_relevante_unica]
            print("ANALISIS DE RELEVANCIA:")
            print(f" -> Atributos causales (Relevantes): {info_relevante_unica}")
            print(f" -> Ruido descartado (Irrelevante): {info_irrelevante}")
            print("\nNUEVA REGLA APRENDIDA (MACRO-OPERADOR):")
            condiciones = " Y ".join(info_relevante_unica)
            print(f" SI [{condiciones}] ENTONCES es '{concepto_objetivo}'")
            return ReglaDominio(concepto_objetivo, info_relevante_unica)
        else:
            print("Fallo en el aprendizaje: El conocimiento del dominio no puede explicar este ejemplo.")
            return None



# DEMOSTRACION: COMPRENDIENDO QUE ES UNA TAZA
if __name__ == "__main__":
    # 1. Definimos la Teoría del Dominio (Conocimiento abstracto previo)
    # El sistema sabe de fisica basica, pero no tiene una regla rapida para detectar tazas.
    conocimiento_previo = [
        ReglaDominio("es_taza", ["sostiene_liquidos", "es_levantable"]),
        ReglaDominio("sostiene_liquidos", ["tiene_concavidad_hacia_arriba", "fondo_plano"]),
        ReglaDominio("es_levantable", ["es_ligero", "tiene_asa"])
    ]
    motor_ebl = AprendizajePorExplicacion(conocimiento_previo)


    # 2. Presentamos un UNICO ejemplo de entrenamiento
    # Es un objeto especifico con muchos atributos, algunos utiles y otros puro ruido.
    ejemplo_observado = [
        "tiene_concavidad_hacia_arriba", 
        "color_rojo",             # Ruido visual
        "fondo_plano",
        "tiene_asa",
        "es_ligero",
        "material_ceramica",      # Ruido de composicion
        "precio_diez_dolares"     # Ruido comercial
    ]
    

    # 3. El sistema realiza Aprendizaje Basado en Explicaciones
    regla_compilada = motor_ebl.aprender_regla_general("es_taza", ejemplo_observado)