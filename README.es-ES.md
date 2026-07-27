## video-translation

video-translation es un proyecto en curso que aprovecha [OpenAI Whisper](https://github.com/openai/whisper) y la API de OpenAI ([TTS](https://platform.openai.com/docs/guides/text-to-speech)) para lograr los siguientes objetivos:

1. Descarga de Video: ✅
2. Extracción de Audio del Video: El formato predeterminado es mp3. ✅
3. Generación de Subtítulos desde Audio y Traducción: ✅
4. Incrustación de Subtítulos (Hard Subs) en Videos: ✅
5. Soporte para Producción de Video en Diferentes Idiomas basado en Subtítulos: En progreso

Por lo tanto, vt añade autónomamente subtítulos en múltiples idiomas tanto a videos online como locales. Las capacidades futuras apuntan a convertir automáticamente las voces del video a varios idiomas. No dudes en seguir y contribuir a este proyecto.

## Setup

Comienza instalando y actualizando mediante poetry:

```bash
poetry install
```

Adicionalmente, asegúrate de tener instalada la herramienta de línea de comandos `ffmpeg` en tu sistema. Está disponible a través de la mayoría de los gestores de paquetes:
```bash
# en Ubuntu o Debian
sudo apt update && sudo apt install ffmpeg

# en Arch Linux
sudo pacman -S ffmpeg

# en MacOS usando Homebrew (https://brew.sh/)
brew install ffmpeg

# en Windows usando Chocolatey (https://chocolatey.org/)
choco install ffmpeg

# en Windows usando Scoop (https://scoop.sh/)
scoop install ffmpeg
```

## Streamlit-based Web UI

La interfaz web de nuestro proyecto, impulsada por Streamlit, permite a los usuarios añadir subtítulos a los videos a través de una interfaz web intuitiva. Esta sección detalla las funciones principales de esta funcionalidad:

1. **Opciones Configurables**: Los usuarios pueden especificar múltiples ajustes, como el modelo de Whisper para el procesamiento de audio, preferencias de idioma, tipos de archivo de video y estilos de subtítulos para adaptarse a diversos requisitos.
2. **Generación Automática de Subtítulos**: La herramienta permite generar subtítulos directamente desde el contenido del video, aprovechando tecnología avanzada de voz a texto para mayor precisión.
3. **Modo de Vista Previa de Subtítulos**: Después de añadir los subtítulos, los usuarios pueden activar un modo de vista previa para ver cómo aparecen los subtítulos en el video real, asegurando una sincronización y estilo adecuados.
4. **Subtítulos Editables con Guardado Automático**: Esta función permite a los usuarios editar los subtítulos y ver los cambios en tiempo real. La opción de 'Auto Save' puede activarse para aplicar las modificaciones instantáneamente.
5. **Descarga de Archivos de Subtítulos**: Una vez creados o editados los subtítulos, los usuarios tienen la opción de descargar estos archivos en diferentes formatos (por ejemplo, SRT, VTT), haciéndolos compatibles con varios reproductores de medios y plataformas.
6. **Exportar Video con Subtítulos**: Los usuarios pueden exportar el video final con los subtítulos incrustados, listo para compartir en diferentes plataformas o para uso personal.

Para iniciar la Interfaz Web:

```bash
poetry run streamlit run webui.py
```

Y abre tu navegador web e ingresa la siguiente dirección para acceder a la Interfaz Web: `http://localhost:8501/`

## Command-line usage

Existen dos tipos principales de uso mediante la línea de comandos:

1. **Generar Archivos de Subtítulos**: Soporta formatos srt y vtt basados en el contenido del video. Puedes usar herramientas de video o funciones de sitios web para añadir estos subtítulos a los videos.
2. **Añadir Subtítulos Directamente a los Videos**: Actualmente soporta tres métodos de adición de subtítulos.

### Generate subtitle files(Supports srt, vtt, json, txt, tsv and all format)

```bash
poetry run vt subtitle --path='https://www.bilibili.com/video/BV1tb4y1L7yA' --language=en --method=whisper --format=vtt --output=/Users/169/Downloads
```

### Download video online and add subtitle

```bash
poetry run python main.py web --url=https://www.youtube.com/watch?v=CqRrByI-ONE
```

El subcomando `web` también admite más opciones, de la siguiente manera:

```bash
poetry run vt web --help
Usage: vt web [OPTIONS]

Options:
  -u, --url TEXT        Video url.  [required]
  -o, --output TEXT     Generated video dir.
  -b, --bilingual TEXT  Use bilingual subtitle. Notice: this option is mutually exclusive
                        with subtitles.
  -s, --subtitles TEXT  Subtitle languages. split by ",". Notice: this option is mutually
                        exclusive with bilingual.
  --help                Show this message and exit.
```

### Use local video and add subtitle

```bash
poetry run vt local --path='/Users/169/Movies/test.mov
```

El subcomando `local` también admite más opciones, de la siguiente manera:

```bash
poetry run vt local --help
Usage: vt local [OPTIONS]

Options:
  -p, --path TEXT       Local file path.  [required]
  -o, --output TEXT     Generated video dir.
  -b, --bilingual TEXT  Use bilingual subtitle. you can specify the subtitle
                        language by `--subtitles`. Notice: this option is
                        mutually exclusive with subtitles.
  -s, --subtitles TEXT  Subtitle languages. split by ",". Notice: this option
                        is mutually exclusive with bilingual.
  --help                Show this message and exit.
```

### Add bilingual subtitles to local video

Utiliza la opción `--bilingual` para crear subtítulos bilingües. Separa los dos idiomas con comas; el primer idioma aparecerá arriba y el segundo abajo.

```bash
poetry run vt local --path="/Users/169/videos/Langchain C3_L6.mp4" --bilingual="cn,en" --output="/Users/169/Downloads"
```

## Custom config

Todos los elementos de configuración residen en [config.py](https://github.com/169/video-translation/blob/main/config.py).

El proyecto también admite una configuración personalizada limitada. Añade un archivo llamado `local_settings.py` dentro del proyecto e incluye los ajustes que desees anular.

Por ejemplo, si el debug predeterminado está establecido en `False` en `config.py`, puedes activar el modo debug añadiendo `debug = True` en local_settings.py:

```bash
cat local_settings.py
debug = True
```
