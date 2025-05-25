
# Analizador Sintáctico en Tkinter

Este es un proyecto en Python que implementa una **interfaz gráfica para un analizador sintáctico básico**, diseñado para validar una sintaxis específica con la palabra reservada `Robot` y métodos como `velocidad`, `base`, `cuerpo` y `garra`.

## 🧠 ¿Qué hace este analizador?

Este programa permite al usuario escribir instrucciones de un lenguaje de garra robótica y analiza si están sintácticamente correctas.  
La primera línea debe declarar el robot con la palabra reservada `Robot`, y las siguientes deben usar un formato como:



r1.velocidad(5)
r1.base(2)



## 🛠 Características

- Interfaz gráfica con `Tkinter`
- Campo de entrada con **número de líneas** al costado
- Análisis sintáctico en tiempo real al presionar el botón "Analizar"
- Validación de estructuras tipo `r1.metodo(valor)`
- Validación de rangos permitidos para cada método
- Muestra errores con mensajes detallados
- Colores para mejorar la legibilidad de resultados (errores en rojo, encabezados en azul)

## 📋 Requisitos

- Python 3.x

No necesitas instalar librerías externas; todo se basa en módulos estándar de Python.

## 🚀 ¿Cómo usarlo?

1. Clona este repositorio o descarga los archivos.
2. Ejecuta el archivo principal:

```bash
python analizador.py
````

3. Escribe instrucciones como las siguientes en el área de texto:

```plaintext
Robot r1
r1.velocidad(5)
r1.base(3)
```

4. Haz clic en **"Analizar"** para validar las instrucciones.

## 📌 Formato esperado

* La **primera línea** debe tener:

  ```
  Robot nombreRobot
  ```
* Las **siguientes líneas** deben tener:

  ```
  nombreRobot.metodo(valor)
  ```

### Métodos válidos y sus rangos:

| Método    | Rango permitido |
| --------- | --------------- |
| velocidad | 1 a 10          |
| base      | 0 a 180         |
| cuerpo    | 0 a 180         |
| garra     | 0 a 180         |

## 🎨 Personalización

Si deseas cambiar el color de fondo de la interfaz, puedes editar esta línea del archivo `analizador.py`:

```python
main_frame = tk.Frame(self.root, padx=10, pady=10, bg='blue')
```

Cámbialo por cualquier color válido, como `'lightblue'` o `'#f0f0f0'`.
