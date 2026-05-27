print("=== BASE DE CONOCIMIENTO Y MOTOR DE INFERENCIA ===\n")
class SistemaExperto:
    def __init__(self):
        # Usamos un conjunto (set) para los hechos, evitando duplicados
        self.hechos = set()
        # Las reglas serán diccionarios con una lista de condiciones y una conclusión
        self.reglas = []



    def agregar_hecho(self, hecho):
        """Añade un hecho irrefutable a la base de conocimiento."""
        self.hechos.add(hecho)
        print(f"Hecho registrado: {hecho}")




    def agregar_regla(self, condiciones, conclusion):
        """
        Añade una regla lógica. 
        Estructura: SI [condición 1] Y [condición 2] ENTONCES [conclusión]
        """
        self.reglas.append({
            "condiciones": condiciones,
            "conclusion": conclusion
        })



    def inferir(self):
        """
        Motor de Inferencia: Encadenamiento hacia Adelante (Forward Chaining).
        Recorre las reglas repetidamente hasta que no se deduzcan nuevos hechos.
        """
        print("\n--- Iniciando Motor de Inferencia ---")
        hubo_nuevos_hechos = True
        iteracion = 1
        


        while hubo_nuevos_hechos:
            hubo_nuevos_hechos = False
            print(f"Iteración {iteracion}:")
            for regla in self.reglas:
                # Comprobamos si TODAS las condiciones de la regla están en nuestros hechos
                condiciones_cumplidas = all(cond in self.hechos for cond in regla["condiciones"])
                # Si se cumplen y la conclusión aún no es un hecho conocido, lo deducimos
                if condiciones_cumplidas and regla["conclusion"] not in self.hechos:
                    self.hechos.add(regla["conclusion"])
                    print(f"  -> NUEVA DEDUCCIÓN: Como tiene {regla['condiciones']}, entonces {regla['conclusion']}")
                    hubo_nuevos_hechos = True # Al encontrar algo nuevo, obligamos a otra iteración   
            if not hubo_nuevos_hechos:
                print("  -> No se pudo deducir nada nuevo.")
            iteracion += 1



# --- EJECUCIÓN Y PRUEBA (Ejemplo: Clasificación de Animales) ---
ia_zoologia = SistemaExperto()



# 1. Definimos las reglas de nuestra Base de Conocimiento
ia_zoologia.agregar_regla(["tiene_pelo"], "es_mamifero")
ia_zoologia.agregar_regla(["da_leche"], "es_mamifero")
ia_zoologia.agregar_regla(["es_mamifero", "come_carne"], "es_carnivoro")
ia_zoologia.agregar_regla(["es_carnivoro", "tiene_rayas_negras", "color_naranja"], "es_tigre")
ia_zoologia.agregar_regla(["es_carnivoro", "tiene_manchas_negras"], "es_leopardo")



print("\n--- Introduciendo Datos del Entorno ---")
# 2. Observamos un animal e introducimos los hechos básicos
ia_zoologia.agregar_hecho("tiene_pelo")
ia_zoologia.agregar_hecho("come_carne")
ia_zoologia.agregar_hecho("color_naranja")
ia_zoologia.agregar_hecho("tiene_rayas_negras")



# 3. Encendemos el motor de inferencia
ia_zoologia.inferir()
print("\n=== BASE DE CONOCIMIENTO FINAL ===")
for h in sorted(ia_zoologia.hechos):
    print(f"- {h}")



print("\n=== ANÁLISIS TÉCNICO ===")
print("1. El sistema no sabía inicialmente que el animal era un mamífero ni un tigre.")
print("2. En la Iteración 1, dedujo 'es_mamifero'.")
print("3. En la Iteración 2, usó la deducción anterior para deducir 'es_carnivoro'.")
print("4. En la Iteración 3, unió todo para deducir 'es_tigre'.")