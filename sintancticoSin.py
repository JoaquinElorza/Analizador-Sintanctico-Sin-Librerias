import tkinter as tk
from tkinter import scrolledtext, messagebox

class analizadorSinComponente:
    def __init__(self, root):  
        self.root = root
        self.create_widgets()

    def palabras_reservadas(self, token):
        return token == 'Robot'

    def es_identificador(self, token):
        return token.isidentifier()

    def es_accion(self, token):
        return token == 'iniciar'

    def es_conector(self, token):
        return token == '.'

    def es_metodo(self, token):
        return token in ['velocidad', 'base', 'cuerpo', 'garra']

    def es_valor(self, token):
        return token.isdigit()

    def parentesis_izquierdo(self, token):
        return token == '('

    def parentesis_derecho(self, token):
        return token == ')'

    def create_widgets(self):
        main_frame = tk.Frame(self.root, padx=10, pady=10, bg='blue')
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(main_frame, text="Ingrese las instrucciones:").pack(anchor=tk.W)

        # Frame para numeración + entrada
        entrada_frame = tk.Frame(main_frame)
        entrada_frame.pack(fill=tk.BOTH, expand=True)

        # Texto con números de línea
        self.line_numbers = tk.Text(entrada_frame, width=4, padx=4, takefocus=0, border=0,
                                    background='lightgrey', state='disabled')
        self.line_numbers.pack(side=tk.LEFT, fill=tk.Y)

        # Texto principal
        self.entrada_text = scrolledtext.ScrolledText(entrada_frame, height=10, wrap=tk.WORD)
        self.entrada_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.entrada_text.bind('<KeyRelease>', self.actualizar_numeracion)

        tk.Button(main_frame, text="Analizar", command=self.leer_entradas,
                  bg="#4CAF50", fg="white").pack(pady=(10, 10))

        tk.Label(main_frame, text="Resultados del análisis:").pack(anchor=tk.W)
        self.resultados_text = scrolledtext.ScrolledText(main_frame, height=15, wrap=tk.WORD)
        self.resultados_text.pack(fill=tk.BOTH, expand=True)

        self.resultados_text.tag_config('error', foreground='red')
        self.resultados_text.tag_config('header', foreground='blue', font=('Arial', 10, 'bold'))

        self.actualizar_numeracion() 

    def actualizar_numeracion(self, event=None):
        self.line_numbers.config(state='normal')
        self.line_numbers.delete(1.0, tk.END)
        lineas = int(self.entrada_text.index('end-1c').split('.')[0])
        for i in range(1, lineas + 1):
            self.line_numbers.insert(tk.END, f'{i}\n')
        self.line_numbers.config(state='disabled')



    def analizar_instruccion(self, texto_completo):
        lineas = [line.strip() for line in texto_completo.split('\n') if line.strip()]
        if not lineas:
            raise ValueError("No se ingresaron instrucciones.")

        tokens_encontrados = []
        rangos_metodos = {
            'velocidad': (1, 10),
            'base': (0, 5),
            'cuerpo': (0, 3),
            'garra': (0, 1)
        }

        # --- Procesar cabecera: Robot r1 ---
        try:
            primera_linea = lineas[0]
            tokens = primera_linea.replace('.', ' . ').replace('(', ' ( ').replace(')', ' ) ').split()
            if len(tokens) != 2:
                raise ValueError("Se esperaba la declaración: Robot r1")
            if not self.palabras_reservadas(tokens[0]):
                raise ValueError("Se esperaba 'Robot' en la línea 1")
            if not self.es_identificador(tokens[1]):
                raise ValueError("Identificador inválido en la línea 1")
            tokens_encontrados.append(('p_reservada', tokens[0]))
            tokens_encontrados.append(('identificador', tokens[1]))
            nombre_robot = tokens[1]
        except ValueError as e:
            raise ValueError(f"Línea 1: {e}")

        # --- Procesar el resto de líneas ---
        for idx, linea in enumerate(lineas[1:], start=2):
            tokens = linea.replace('.', ' . ').replace('(', ' ( ').replace(')', ' ) ').split()
            temp_tokens = [] # Lista temporal para almacenar tokens de la línea actual

            for token in tokens:
                if self.es_conector(token):
                    temp_tokens.append(('conector', token))
                elif self.es_metodo(token):
                    temp_tokens.append(('metodo', token))
                elif self.parentesis_izquierdo(token):
                    temp_tokens.append(('parentesisI', token))
                elif self.es_valor(token):
                    temp_tokens.append(('valor', token))
                elif self.parentesis_derecho(token):
                    temp_tokens.append(('parentesisD', token))
                elif self.es_identificador(token):
                    temp_tokens.append(('identificador', token))
                else:
                    raise ValueError(f"Línea {idx}: Token no reconocido: {token}")

            # Validación de la estructura: r1.metodo(valor)
            if len(temp_tokens) != 6:
                raise ValueError(f"Línea {idx}: Formato incorrecto, se esperaba 'r1.metodo(valor)'")

            tipo1, val1 = temp_tokens[0] # identificador
            tipo2, val2 = temp_tokens[1] # conector
            tipo3, val3 = temp_tokens[2] # metodo
            tipo4, val4 = temp_tokens[3] # parentesis
            tipo5, val5 = temp_tokens[4] # valor
            tipo6, val6 = temp_tokens[5] # parentesis

            if tipo1 != 'identificador' or val1 != nombre_robot:
                raise ValueError(f"Línea {idx}: Se esperaba el identificador '{nombre_robot}'")
            if tipo2 != 'conector' or val2 != '.':
                raise ValueError(f"Línea {idx}: Se esperaba '.' después del identificador")
            if tipo3 != 'metodo' or self.es_metodo(val3) == False:
                print(f"[DEBUG] Token exacto: {repr(token)}")
                raise ValueError(f"Línea {idx}: Se esperaba un método válido")
            if tipo4 != 'parentesisI' or val4 != '(':
                raise ValueError(f"Línea {idx}: Se esperaba '(' después del método")
            if tipo5 != 'valor':
                raise ValueError(f"Línea {idx}: Se esperaba un valor dentro del paréntesis")
            if tipo6 != 'parentesisD' or val6 != ')':
                raise ValueError(f"Línea {idx}: Se esperaba ')' al final")
            

            # Obtener valor dentro del paréntesis
            try:
                valor_token = val5
                if not self.es_valor(valor_token):
                    raise ValueError(f"Línea {idx}: Valor inválido dentro del paréntesis")
                valor_int = int(valor_token)
                if val3 in rangos_metodos:
                    minimo, maximo = rangos_metodos[val3]
                    if not (minimo <= valor_int <= maximo):
                        raise ValueError(f"Línea {idx}: El valor de '{val3}' debe estar entre {minimo} y {maximo}")
                else:
                    raise ValueError(f"Línea {idx}: Método no reconocido: {val3}")
            except IndexError:
                raise ValueError(f"Línea {idx}: No se encontró el valor dentro del paréntesis")

            tokens_encontrados.extend(temp_tokens)
            tokens_encontrados.append(('valor', valor_token))

        return tokens_encontrados




    def leer_entradas(self):
        self.resultados_text.delete(1.0, tk.END)

        texto = self.entrada_text.get(1.0, tk.END).strip()
        if not texto:
            messagebox.showwarning("Advertencia", "Por favor ingrese al menos una instrucción.")
            return

        try:
            self.analizar_instruccion(texto)
            self.resultados_text.insert(tk.END, "Instrucción válida.\n", 'header')
        except ValueError as e:
            self.resultados_text.insert(tk.END, f"Error: {e}\n", 'error')



if __name__ == "__main__":  
    Raiz = tk.Tk()
    Raiz.title("Analizador Sintactico Sin Componentes")
    Raiz.geometry("800x0700")
    app = analizadorSinComponente(Raiz)
    Raiz.mainloop()