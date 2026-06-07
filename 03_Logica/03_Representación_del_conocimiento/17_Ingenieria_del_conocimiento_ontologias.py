# Importamos la librería estándar para ontologías en Python
from owlready2 import *
def crear_ontologia_universidad():
    print("___INICIANDO MOTOR DE INGENIERÍA DEL CONOCIMIENTO___")



    # 1. CREAR EL UNIVERSO (Ontología en memoria)
    # Se le asigna una URL (IRI) única que sirve como identificador global
    onto = get_ontology("http://simulador.miuniversidad.org/onto.owl")



    # Entramos al contexto de nuestra nueva ontología
    with onto:
        print("1 Definiendo Clases (Conceptos)...")
        # Definimos las jerarquías de clases. 
        # 'Thing' es la clase raíz absoluta en OWL (Todo es una "Cosa")
        class Persona(Thing): pass
        class Estudiante(Persona): pass
        class Profesor(Persona): pass
        class Curso(Thing): pass



        print("2 Definiendo Propiedades (Reglas lógicas)...")
        # 'ObjectProperty' define relaciones entre dos individuos
        class estudia(ObjectProperty):
            domain = [Estudiante]  # Solo un estudiante puede "estudiar"
            range  = [Curso]       # Solo se pueden estudiar "cursos"
        class imparte(ObjectProperty):
            domain = [Profesor]    # Solo un profesor puede "impartir"
            range  = [Curso]       # Solo se pueden impartir "cursos"



        print("3 Creando Individuos (Instancias reales)...")
        # Creamos materias
        curso_ia = Curso("Inteligencia_Artificial")
        curso_datos = Curso("Bases_de_Datos")



        # Creamos personas y les asignamos relaciones lógicas
        estudiante1 = Estudiante("Maria")
        estudiante1.estudia = [curso_ia, curso_datos]
        estudiante2 = Estudiante("Carlos")
        estudiante2.estudia = [curso_ia]
        profesor1 = Profesor("Dr_Turing")
        profesor1.imparte = [curso_ia, curso_datos]
    print("\nOntología creada exitosamente. ¡El conocimiento está estructurado!\n")
    return onto



def consultar_conocimiento(onto):
    """Función para realizar consultas al Grafo de Conocimiento"""
    print("=====================================================")
    print("REALIZANDO CONSULTAS SEMÁNTICAS")
    print("=====================================================")
    


    # 1. ¿Cuáles son las clases principales que existen en nuestro mundo?
    print("\nConceptos (Clases) definidos en el universo:")
    for clase in onto.classes():
        print(f" - {clase.name}")



    # 2. Consultar individuos y sus relaciones
    print("\nConsultando a los estudiantes y qué hacen:")
    for est in onto.Estudiante.instances():
        # Extraemos los nombres de los cursos que estudia
        materias = [curso.name for curso in est.estudia]
        print(f"{est.name} está inscrito(a) en: {materias}")



    print("\nConsultando a los profesores y qué hacen:")
    for prof in onto.Profesor.instances():
        materias = [curso.name for curso in prof.imparte]
        print(f"{prof.name} imparte las materias de: {materias}")



# --- Ejecución del Programa ---
mi_ontologia = crear_ontologia_universidad()
consultar_conocimiento(mi_ontologia)
# Opcional: Puedes guardar este universo en un archivo físico estandarizado
# mi_ontologia.save(file="universidad.owl", format="rdfxml")