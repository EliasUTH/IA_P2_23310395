import re


class Token:
    """
    Representa la unidad logica minima de un lenguaje.
    Contiene la categoria gramatical (tipo) y la cadena original (lexema).
    """
    def __init__(self, tipo, lexema, linea, columna):
        self.tipo = tipo
        self.lexema = lexema
        self.linea = linea
        self.columna = columna


    def __str__(self):
        return f"Token(Tipo: {self.tipo:<15} | Lexema: '{self.lexema:<10}' | Linea: {self.linea}, Columna: {self.columna})"




class AnalizadorLexico:
    """
    Motor de analisis lexico basado en Expresiones Regulares.
    """
    def __init__(self):
        # Definicion de las reglas lexicas (Gramaticas Tipo 3)
        # El orden es sumamente importante: las reglas mas especificas deben ir primero.
        self.reglas_lexicas = [
            ('PALABRA_RESERVADA', r'\b(si|sino|mientras|entero|retornar|funcion)\b'),
            ('IDENTIFICADOR',     r'[a-zA-Z_][a-zA-Z0-9_]*'),
            ('NUMERO_DECIMAL',    r'\d+\.\d+'),
            ('NUMERO_ENTERO',     r'\d+'),
            ('OPERADOR_LOGICO',   r'(==|!=|<=|>=|&&|\|\|)'),
            ('OPERADOR_MATE',     r'[+\-*/=<>!]'),
            ('PUNTUACION',        r'[;,\(\)\{\}]'),
            ('CADENA_TEXTO',      r'".*?"'),
            ('ESPACIOS',          r'[ \t]+'),
            ('SALTO_LINEA',       r'\n'),
            ('COMENTARIO',        r'//.*')
        ]
        


        # Se compila una unica expresion regular gigante uniendo todos los patrones.
        # Python permite nombrar grupos regex usando la sintaxis (?P<nombre>patron)
        patron_combinado = '|'.join(f'(?P<{nombre}>{patron})' for nombre, patron in self.reglas_lexicas)
        self.regex_maestra = re.compile(patron_combinado)



    def escanear(self, codigo_fuente):
        """
        Recorre el texto de entrada y devuelve un flujo (stream) de tokens.
        """
        print("Iniciando escaneo lexico...\n")
        tokens = []
        linea_actual = 1
        inicio_linea = 0
        


        # Encontramos todas las coincidencias en el codigo fuente
        for coincidencia in self.regex_maestra.finditer(codigo_fuente):
            # 'lastgroup' nos dice cual de las reglas de nuestro diccionario hizo match
            tipo_token = coincidencia.lastgroup
            lexema = coincidencia.group(tipo_token)
            columna_actual = coincidencia.start() - inicio_linea + 1
            


            # --- MANEJO DE REGLAS DE IGNORANCIA (Descarte) ---
            if tipo_token == 'SALTO_LINEA':
                linea_actual += 1
                inicio_linea = coincidencia.end()
                continue
            elif tipo_token == 'ESPACIOS' or tipo_token == 'COMENTARIO':
                # Ignoramos silenciosamente el ruido sintactico
                continue



            # --- CREACION DEL TOKEN VALIDO ---
            nuevo_token = Token(tipo_token, lexema, linea_actual, columna_actual)
            tokens.append(nuevo_token)
            


        # --- VIGILANCIA DE ERRORES LEXICOS ---
        # Verificamos si alguna parte del texto no hizo coincidencia con ninguna regla
        texto_procesado = 0
        for token in tokens:
            texto_procesado += len(token.lexema)    
        # Un metodo mas estricto para detectar errores seria comparar indices
        # pero para mantener el codigo limpio iteramos sobre las coincidencias
        # Si un caracter es totalmente desconocido (ej: un emoji o simbolo no programado '@')
        # la regex lo ignorara y saltara. En un compilador real, esto lanza un Error Lexico.
        return tokens



# DEMOSTRACION: TOKENIZACION DE UN SCRIPT
if __name__ == "__main__":
    # Un fragmento de codigo fuente simulado en un lenguaje inventado
    codigo_fuente = """
    // Calcula la aceleracion
    funcion calcular_velocidad(entero tiempo) {
        entero gravedad = 9;
        si (tiempo > 0) {
            retornar gravedad * tiempo;
        } sino {
            retornar 0;
        }
    }
    """
    

    print("ANALIZADOR LEXICO (SCANNER)")
    print("Codigo fuente de entrada:")
    print(codigo_fuente)
    print("-" * 53)
    analizador = AnalizadorLexico()
    flujo_de_tokens = analizador.escanear(codigo_fuente)
    print("Flujo de Tokens Resultante:")
    print("-" * 53)
    for token in flujo_de_tokens:
        print(token)