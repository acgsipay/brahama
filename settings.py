#!/usr/bin/python
# -*- coding: utf-8 -*-
import os

from tornado.options import define, options, parse_command_line

ROOT_PATH = os.getcwd()
BASE_PATH = os.path.dirname(os.path.abspath(__file__))

# Definición de las opciones de configuración
define('port', default=8888, help='Puerto', type=int)
define('env', default='production', help='Entorno')
define('debug', default=False, help='Modo depuracion', type=bool)

parse_command_line()

# Configuración de la aplicación
params = {}

# Indicar método depuración (nunca en producción)
params['debug'] = options.debug

# Recarga los ficheros de la aplicación en tiempo de ejecución
params['autoreload'] = params['debug']

# Ruta a los ficheros estaticos
params['static_path'] = os.path.join(BASE_PATH, 'static')

# Cachear ficheros estaticos (siempre en producción)
params['static_hash_cache'] = options.env == 'production'

# Ruta a las plantillas de la aplicación
params['template_path'] = os.path.join(BASE_PATH, 'template')

# Compilar plantillas (siempre en producción)
params['compiled_template_cache'] = options.env == 'production'

# Comprimir respuesta (siempre en producción)
params['compress_response'] = options.env == 'production'

# Ruta al directorio de almacenamiento
params['storage.path'] = os.path.join(BASE_PATH, 'storage')

# Ruta al directorio de almacenamiento de certificados
params['vault.path'] = os.path.join(params['storage.path'], 'vault')

# Ruta al directorio de almacenamiento de trazas
params['log.path'] = os.path.join(params['storage.path'], 'logs')

# Nombre del fichero de trazas general
params['log.file.main'] = os.path.join(params['log.path'], 'main.log')

# Nombre del fichero de trazas de error
params['log.file.error'] = os.path.join(params['log.path'], 'error.log')

# Ruta al directorio de los ficheros de configuración
settings['config.path'] = os.path.join(params['storage.path'], 'config')

# Fichero de configuración principal
settings['config.file.main'] = os.path.join(settings['config.path'], 'main.conf')

# Fichero de configuración por entorno
settings['config.file.env'] = os.path.join(settings['config.path'], 'main.environment.conf')

# Carga del gestor de ficheros de configuración
configuration = ConfigParser.SafeConfigParser(allow_no_value=True)
configuration.read([settings['config.file.main'], settings['config.file.env']])

# Fichero certificado Clave Privada
settings['secure.cert'] = os.path.join(settings['vault.path'], configuration.get('secure', 'cert'))

# Fichero certificado Clave Publica
settings['secure.key'] = os.path.join(settings['vault.path'], configuration.get('secure', 'key'))

# Fichero CA
settings['secure.ca'] = os.path.join(settings['vault.path'], configuration.get('secure', 'ca'))

# Servidor de memcached
settings['memcached.host'] = '127.0.0.1'

# Puerto de memcached
settings['memcached.port'] = '11211'

# Tiempo de expiración (importante en producción 5 minutos)
settings['memcached.expiration'] = 300 if options.env == 'production' else 86400
