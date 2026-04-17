# LSC App - Traductor de Lengua de Señas Colombiana 🤟

Sistema de traducción de Lengua de Señas Colombiana (LSC) mediante Inteligencia Artificial, desarrollado con Python y PyQt5.

## Funcionalidades

- **Seña → Texto:** Detecta señas del alfabeto dactilológico colombiano en tiempo real y las convierte a texto
- **Seña → Voz:** Lee en voz alta el texto formado por las señas
- **Voz → Seña:** Escucha lo que decís y muestra las imágenes de las señas correspondientes
- **Entrenamiento:** Capturá tus propios ejemplos para entrenar el modelo

## Requisitos

- Python 3.10.x
- Cámara web
- Micrófono
- Conexión a internet (para reconocimiento de voz)

## Instalación

**1. Clonar el repositorio**
```bash
git clone https://github.com/tuusuario/LSC-App.git
cd LSC-App
```

**2. Crear entorno virtual**
```bash
python -m venv venv
```

**3. Activar el entorno virtual**
```bash
# Windows
venv\Scripts\activate
```

**4. Instalar dependencias**
```bash
pip install -r requirements.txt
```

**5. Ejecutar la aplicación**
```bash
python main.py
```

## Estructura del proyecto

```
LSC-App/
├── main.py                 # Punto de entrada
├── requirements.txt        # Dependencias
├── modules/
│   ├── detector.py         # Detección de manos con MediaPipe
│   ├── classifier.py       # Clasificador KNN
│   ├── voice.py            # Módulo de voz
│   ├── sentence_builder.py # Constructor de oraciones
│   └── sign_display.py     # Visualización de señas
├── ui/
│   └── main_window.py      # Interfaz gráfica
├── assets/
│   └── signs/              # Imágenes del alfabeto LSC
└── data/
    └── dataset.json        # Dataset de entrenamiento (generado al entrenar)
```

## Entrenamiento del modelo

1. Abrí la pestaña **Entrenar Modelo**
2. Iniciá la cámara
3. Escribí la letra que querés entrenar
4. Usá **Ráfaga (30 ejemplos)** para capturar rápidamente
5. Repetí con cada letra del alfabeto
6. Mínimo 30 ejemplos por letra para buena precisión

## Tecnologías usadas

- **Python 3.10**
- **MediaPipe** — Detección de manos y landmarks
- **KNN** — Clasificación de señas
- **PyQt5** — Interfaz gráfica
- **pyttsx3** — Texto a voz
- **SpeechRecognition** — Voz a texto
- **OpenCV** — Procesamiento de video

## Letras disponibles

El dataset incluye imágenes de las letras estáticas del alfabeto LSC:
**A, B, C, D, E, F, I, K, L, M, N, O, P, Q, R, T, U, V, W, X, Y**

Las letras dinámicas (G, H, J, Ñ, S, Z) están en desarrollo para futuras versiones.

## Desarrolladores

- David Santiago Granados Cárdenas

## Proyecto base

Desarrollado como continuación del proyecto **TV002-2025** del Tecnoparque SENA Nodo Boyacá.
