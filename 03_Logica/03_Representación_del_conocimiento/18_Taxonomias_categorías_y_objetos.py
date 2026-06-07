class Objeto:
    """Representa un elemento único y real en el mundo (Instancia)"""
    def __init__(self, nombre, atributos=None):
        self.nombre = nombre
        self.atributos = atributos if atributos else {}



    def __str__(self):
        # Muestra el nombre y sus atributos si los tiene
        attr_str = f" {self.atributos}" if self.atributos else ""
        return f"{self.nombre}{attr_str}"



class Categoria:
    """Representa una agrupación conceptual de cosas (Clase/Categoría)"""
    def __init__(self, nombre):
        self.nombre = nombre
        self.subcategorias = []
        self.objetos = []



    def agregar_subcategoria(self, subcategoria):
        self.subcategorias.append(subcategoria)
        return subcategoria # Retornamos para poder encadenar llamadas



    def agregar_objeto(self, objeto):
        self.objetos.append(objeto)



    def mostrar_arbol(self, nivel=0):
        """Imprime la taxonomía completa de forma recursiva simulando un árbol visual"""
        sangria = "    " * nivel
        print(f"{sangria}[{self.nombre}]")
        



        # Primero imprimimos los objetos directos de esta categoría
        for obj in self.objetos:
            print(f"{sangria} {obj}")    
        # Luego entramos a las subcategorías recursivamente
        for subcat in self.subcategorias:
            subcat.mostrar_arbol(nivel + 1)




    def buscar_objeto(self, nombre_objeto, ruta_actual=None):
        """Busca un objeto en el árbol y devuelve la ruta taxonómica para llegar a él"""
        if ruta_actual is None:
            ruta_actual = []  
        ruta_actual.append(self.nombre)



        # Revisamos si el objeto está aquí
        for obj in self.objetos:
            if obj.nombre.lower() == nombre_objeto.lower():
                return ruta_actual + [obj.nombre]



        # Si no está, buscamos en las subcategorías
        for subcat in self.subcategorias:
            resultado = subcat.buscar_objeto(nombre_objeto, ruta_actual.copy())
            if resultado:
                return resultado       
        return None

print("___CONSTRUYENDO ÁRBOL TAXONÓMICO___")



# 1. Creamos la Categoría Raíz
raiz = Categoria("Catálogo General")



# 2. Creamos ramas principales (Categorías)
cat_tecnologia = Categoria("Tecnología")
cat_hogar = Categoria("Hogar")
raiz.agregar_subcategoria(cat_tecnologia)
raiz.agregar_subcategoria(cat_hogar)



# 3. Creamos subcategorías más específicas
cat_computacion = cat_tecnologia.agregar_subcategoria(Categoria("Computación"))
cat_telefonia = cat_tecnologia.agregar_subcategoria(Categoria("Telefonía"))
cat_muebles = cat_hogar.agregar_subcategoria(Categoria("Muebles"))



# 4. Poblamos la taxonomía con Objetos (Instancias)
cat_computacion.agregar_objeto(Objeto("Laptop Dell XPS", {"RAM": "16GB", "CPU": "i7"}))
cat_computacion.agregar_objeto(Objeto("MacBook Air M2", {"Color": "Plata"}))
cat_telefonia.agregar_objeto(Objeto("iPhone 15 Pro", {"Almacenamiento": "256GB"}))
cat_telefonia.agregar_objeto(Objeto("Samsung Galaxy S24", {"Batería": "5000mAh"}))
cat_muebles.agregar_objeto(Objeto("Sofá de Cuero 3 Plazas"))
cat_muebles.agregar_objeto(Objeto("Mesa de Centro de Roble"))



print("1 VISTA GENERAL DEL ÁRBOL DE CONOCIMIENTO:")
raiz.mostrar_arbol()
print("2 MOTOR DE BÚSQUEDA Y CLASIFICACIÓN:")


objetivo = "iPhone 15 Pro"
print(f"\nBuscando dónde se clasifica el objeto: '{objetivo}'...")
ruta = raiz.buscar_objeto(objetivo)



if ruta:
    # Unimos la ruta con flechas para mostrar el linaje taxonómico
    linaje = " ➔ ".join(ruta)
    print(f"¡Objeto encontrado!")
    print(f"Clasificación (Linaje): {linaje}")
else:
    print(f"El objeto no existe en la taxonomía.")