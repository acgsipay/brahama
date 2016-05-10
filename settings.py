#!/usr/bin/python
# -*- coding: utf-8 -*-
import os

from tornado.options import define, options, parse_command_line

ROOT = os.path.dirname(os.path.abspath(__file__))

# Definición de las opciones de configuración
define('port', default=8888, help='Puerto', type=int)
define('env', default='production', help='Entorno')

parse_command_line()

# Configuración de la aplicación
params = {}

# Indicar método depuración (nunca en producción)
params['debug'] = options.env != 'production'

# Recarga los ficheros de la aplicación en tiempo de ejecución
params['autoreload'] = params['debug']

# Ruta a los ficheros estaticos
params['static_path'] = os.path.join(ROOT, 'static')

# Cachear ficheros estaticos (siempre en producción)
params['static_hash_cache'] = options.env == 'production'

# Ruta a las plantillas de la aplicación
params['template_path'] = os.path.join(ROOT, 'template')

# Compilar plantillas (siempre en producción)
params['compiled_template_cache'] = options.env == 'production'

# Comprimir respuesta (siempre en producción)
params['compress_response'] = options.env == 'production'

# Ruta al directorio de almacenamiento
params['storage_path'] = os.path.join(ROOT, 'storage')

# Ruta al directorio de almacenamiento de certificados
params['vault_path'] = os.path.join(params['storage_path'], 'vault')

# Ruta al directorio de almacenamiento de trazas
params['log_path'] = os.path.join(params['storage_path'], 'logs')

# Nombre del fichero de trazas general
params['log_main'] = os.path.join(params['log_path'], 'main.log')

# Nombre del fichero de trazas de error
params['log_error'] = os.path.join(params['log_path'], 'error.log')