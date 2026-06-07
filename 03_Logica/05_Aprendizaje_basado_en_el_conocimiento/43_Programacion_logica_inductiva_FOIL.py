import math
import copy


class MotorFOIL:
    """
    Simulador del algoritmo FOIL para aprender reglas logicas de primer orden.
    """
    def __init__(self, base_conocimiento):
        # La Base de Conocimiento (Background Knowledge) contiene los hechos del dominio
        self.base_conocimiento = base_conocimiento



    def inicializar_ligaduras(self, variables_objetivo, ejemplos):
        """
        Convierte una lista de tuplas en una lista de diccionarios (Ligaduras o Bindings).
        Ejemplo: variables_objetivo=['X', 'Y'], ejemplo=('juan', 'carlos')
        Resultado: {'X': 'juan', 'Y': 'carlos'}
        """
        ligaduras = []
        for ejemplo in ejemplos:
            ligadura = {}
            for i in range(len(variables_objetivo)):
                ligadura[variables_objetivo[i]] = ejemplo[i]
            ligaduras.append(ligadura)
        return ligaduras


    def evaluar_literal(self, ligaduras_actuales, literal_candidato):
        """
        Intenta agregar un predicado logico a la regla actual.
        Filtra las ligaduras que no cumplen el predicado e introduce nuevas variables.
        """
        nombre_pred, var1, var2 = literal_candidato
        nuevas_ligaduras = []
        

        # Iteramos sobre todos los universos posibles (ligaduras) actuales
        for ligadura in ligaduras_actuales:
            # Buscamos en nuestra base de datos los hechos reales para este predicado
            hechos_conocidos = self.base_conocimiento.get(nombre_pred, [])
            

            for arg1_hecho, arg2_hecho in hechos_conocidos:
                # Obtenemos los valores de las variables en la ligadura actual (si existen)
                val_var1 = ligadura.get(var1)
                val_var2 = ligadura.get(var2)
                

                # Una variable coincide si ya estaba asignada a ese valor, 
                # o si es una variable nueva (None) que apenas estamos introduciendo (Ej: 'Z')
                coincide1 = (val_var1 is None) or (val_var1 == arg1_hecho)
                coincide2 = (val_var2 is None) or (val_var2 == arg2_hecho)
                

                if coincide1 and coincide2:
                    # Si coincide, se crea un nuevo universo derivado con las variables unificadas
                    nueva_ligadura = ligadura.copy()
                    nueva_ligadura[var1] = arg1_hecho
                    nueva_ligadura[var2] = arg2_hecho


                    # Evitamos ligaduras tautologicas donde X=X (ej. padre(juan, juan))
                    if nueva_ligadura[var1] != nueva_ligadura.var2 if hasattr(nueva_ligadura, 'var2') else True:
                        nuevas_ligaduras.append(nueva_ligadura)
                    
        return nuevas_ligaduras


    def calcular_ganancia_foil(self, p0, n0, p1, n1):
        """
        Mide cuanta informacion se gana al agregar un literal a la regla.
        Formula: p1 * ( Log2(p1/(p1+n1)) - Log2(p0/(p0+n0)) )
        """
        if p1 == 0: 
            return 0.0 # Si el literal elimina todos los ejemplos positivos, es inutil 
        precision_inicial = p0 / (p0 + n0)
        precision_final = p1 / (p1 + n1)
    

        # Prevenir logaritmo de cero
        if precision_inicial == 0 or precision_final == 0:
            return 0.0 
        info_inicial = math.log2(precision_inicial)
        info_final = math.log2(precision_final)
        ganancia = p1 * (info_final - info_inicial)
        return ganancia


    def inducir_regla(self, predicado_objetivo, vars_objetivo, ejemplos_pos, ejemplos_neg, literales_candidatos):
        """
        Bucle interno de FOIL: Construye una regla agregando literales vorazmente
        hasta que ningun ejemplo negativo sea cubierto.
        """
        print(f"Iniciando induccion para: {predicado_objetivo}({', '.join(vars_objetivo)})")
        ligaduras_pos = self.inicializar_ligaduras(vars_objetivo, ejemplos_pos)
        ligaduras_neg = self.inicializar_ligaduras(vars_objetivo, ejemplos_neg)
        cuerpo_regla = []
        


        # Mientras la regla siga cubriendo ejemplos negativos
        while len(ligaduras_neg) > 0:
            p0 = len(ligaduras_pos)
            n0 = len(ligaduras_neg)
            mejor_ganancia = -1.0
            mejor_literal = None
            mejores_lig_pos = []
            mejores_lig_neg = []
            

            # Evaluamos todos los posibles predicados que podriamos agregar a la regla
            for candidato in literales_candidatos:
                # Simulamos agregar este literal
                nuevas_lig_pos = self.evaluar_literal(ligaduras_pos, candidato)
                nuevas_lig_neg = self.evaluar_literal(ligaduras_neg, candidato)
                p1 = len(nuevas_lig_pos)
                n1 = len(nuevas_lig_neg)
                ganancia = self.calcular_ganancia_foil(p0, n0, p1, n1)
                


                # Mostrar el analisis interno del algoritmo
                literal_str = f"{candidato[0]}({candidato[1]}, {candidato[2]})"
                print(f" -> Evaluando {literal_str:<15} | Pos:{p1} Neg:{n1} | Ganancia: {ganancia:.4f}")
                


                if ganancia > mejor_ganancia:
                    mejor_ganancia = ganancia
                    mejor_literal = candidato
                    mejores_lig_pos = nuevas_lig_pos
                    mejores_lig_neg = nuevas_lig_neg
            


            if mejor_literal is None or mejor_ganancia <= 0:
                print("Fallo: No se encontro ningun literal que mejore la regla.")
                break


            # Agregamos el ganador absoluto a la regla y actualizamos el estado del universo
            cuerpo_regla.append(mejor_literal)
            ligaduras_pos = mejores_lig_pos
            ligaduras_neg = mejores_lig_neg
            lit_str = f"{mejor_literal[0]}({mejor_literal[1]}, {mejor_literal[2]})"
            print(f"\n[!] LITERAL SELECCIONADO: {lit_str}")
            print(f"  Estado actual: Positivos cubiertos = {len(ligaduras_pos)}, Negativos cubiertos = {len(ligaduras_neg)}\n")


        # Formatear y devolver la regla logica final
        cuerpo_str = " Y ".join([f"{pred}({v1}, {v2})" for pred, v1, v2 in cuerpo_regla])
        regla_final = f"SI {cuerpo_str} ENTONCES {predicado_objetivo}({vars_objetivo[0]}, {vars_objetivo[1]})"
        return regla_final



# DEMOSTRACION: DESCUBRIENDO QUE ES UN ABUELO
if __name__ == "__main__":
    # 1. Base de Conocimiento Extensional (Hechos del mundo real)
    # padre(X, Y) significa "X es padre de Y"
    hechos_familiares = {
        'padre': [
            ('arturo', 'juan'), 
            ('juan', 'pedro'), 
            ('juan', 'maria'), 
            ('pedro', 'carlos')
        ],
        'madre': [
            ('carmen', 'pedro')
        ]
    }
    


    # 2. Datos de entrenamiento para el concepto objetivo "abuelo(X, Y)"
    positivos = [
        ('arturo', 'pedro'), # Arturo es abuelo de Pedro
        ('arturo', 'maria'), # Arturo es abuelo de Maria
        ('juan', 'carlos')   # Juan es abuelo de Carlos
    ]
    


    # Ejemplos que la IA no debe confundir
    negativos = [
        ('juan', 'pedro'),   # Juan es PADRE de Pedro, no abuelo
        ('pedro', 'carlos'), # Pedro es PADRE de Carlos, no abuelo
        ('arturo', 'juan'),  # Arturo es PADRE de Juan, no abuelo
        ('carlos', 'juan')   # Relacion inversa erronea
    ]
    


    # 3. Espacio de hipotesis (Combinatoria de predicados y variables que la IA puede usar)
    # Nota como ILP permite inventar una variable intermedia 'Z' para enlazar entidades
    candidatos = [
        ('padre', 'X', 'Y'), # ¿Es simplemente el padre?
        ('padre', 'Y', 'X'), # ¿Es el hijo?
        ('padre', 'X', 'Z'), # "X es padre de un tal Z..." (Introduccion de variable Z)
        ('padre', 'Z', 'Y'), # "Un tal Z es padre de Y..."
        ('madre', 'X', 'Z')
    ]
    


    # 4. Ejecucion de FOIL
    print("ALGORITMO FOIL: PROGRAMACION LOGICA INDUCTIVA\n")
    aprendiz = MotorFOIL(hechos_familiares)
    regla_descubierta = aprendiz.inducir_regla(
        predicado_objetivo="abuelo",
        vars_objetivo=['X', 'Y'],
        ejemplos_pos=positivos,
        ejemplos_neg=negativos,
        literales_candidatos=candidatos
    )


    print("REGLA RELACIONAL APRENDIDA:")
    print(regla_descubierta)