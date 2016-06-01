#!/usr/bin/python
# -*- coding: utf-8 -*-
from uuid import uuid1
import json

from tornado.web import RequestHandler
from tornado.escape import json_decode
from core.utils.collections import implode, args


class BaseHandler(RequestHandler, BaseHandlerParser, BaseHandlerValidator, BaseHandlerFormatter, BaseHandlerError):
    def initialize(self):
        self.uuid = str(uuid1())

        self.logger = self.application['logger']
        self.cache = self.application['memcache']
        self.soap = self.application['soap.sipay_ecommerce']

        self.params = {k: self.get_argument(k) for k in self.request.arguments}

    def prepare(self):
        if "Content-Type" in self.headers and self.headers["Content-Type"].startswith('application/json'):
            try:
                params = json_decode(self.request.body)
                self.params.update(params)
            except ValueError:
                self.data_entry_parse_error()

    def get_cache_data(self, key):
        data = False

        try:
            data = self.cache.get(key)
        except:
            self.get_cache_data_error(key)
        finally:
            return data


class BaseHandlerError(object):
    LOGGER_FORMAT = 'uuid=%s; type=%s; code=%s; detail=%s; fromip=%s; %s'

    def log_error(self, type, code, detail, **kwargs):
        self.logger.error(self.LOGGER_FORMAT % (self.uuid, type, code, detail, self.remote_ip, implode(kwargs)))

    def log_warning(self, type, code, detail, **kwargs):
        self.logger.warning(self.LOGGER_FORMAT % (self.uuid, type, code, detail, self.remote_ip, implode(kwargs)))

    def log_info(self, type, code, detail, **kwargs):
        self.logger.info(self.LOGGER_FORMAT % (self.uuid, type, code, detail, self.remote_ip, implode(kwargs)))

    def log_debug(self, type, code, detail, **kwargs):
        self.logger.debug(self.LOGGER_FORMAT % (self.uuid, type, code, detail, self.remote_ip, implode(kwargs)))

    def data_entry_mandatory_error(self, key):
        type = 'data_entry.mandatory'
        code = 'E-0001'
        detail = 'Campo obligatorio no disponible'

        self.log_error(type=type, code=code, detail=detail, field_name=key)
        self.data_entry_mandatory_error_display(key)

    def data_entry_mandatory_error_display(self, key):
        self.finish({
            'type': 'error',
            'code': 'CERR001',
            'message': 'required_field_missing',
            'payload': {}
        })

    def data_entry_validation_error(self, key, rule, strict):
        type = 'data_entry.validation'
        code = 'E-0002'
        detail = 'Formato de campo incorrecto'

        mode = 'strict' if strict else 'nonstrict'

        self.log_error(type=type, code=code, detail=detail, field_name=key, validation=rule, mode=mode)
        self.data_entry_validation_error_display(key, rule, strict)

    def data_entry_validation_error_display(self, key, rule, strict):
        self.finish({
            'type': 'error',
            'code': 'CERR002',
            'message': 'incorrect_field_format',
            'payload': {}
        })

    def data_entry_parse_error(self):
        type = 'data_entry.parse'
        code = 'E-0003'
        detail = 'Cuerpo de la petición en el formato incorrecto'

        self.log_error(type=type, code=code, detail=detail, header=self.headers["Content-Type"], body=self.request.body)
        self.data_entry_parse_error_display()

    def data_entry_validation_error_display(self):
        self.finish({
            'type': 'error',
            'code': 'CERR003',
            'message': 'incorrect_body_format',
            'payload': {}
        })

    def get_cache_data_error(self, key):
        type = 'data_persistence.cache'
        code = 'E-0004'
        detail = 'Error al obtener información de cache'
        self.log_error(type=type, code=code, detail=detail, key=key)
        self.get_cache_data_error_display(key)

    def get_cache_data_error_display(self):
        self.finish({
            'type': 'error',
            'code': 'CERR004',
            'message': 'request_expired',
            'payload': {}
        })

    def server_not_response_error(self, protocol, server, method, args):
        type = 'server.response'
        code = 'E-0005'
        detail = 'Respuesta de servidor incorrecta'
        self.log_error(type=type, code=code, detail=detail, protocol=protocol, server=server, method=method, args=args)
        self.server_not_response_error(protocol, server, method, args)

    def server_not_response_error_display(self):
        self.finish({
            'type': 'error',
            'code': 'CERR005',
            'message': 'busy_server',
            'payload': {}
        })


class BaseHandlerFormatter(object):
    FORMATTER_FALSE_VALUES = ('false', 'no', 'off', '0', 0, False, None)
    FORMATTER_TRUE_VALUES = ('true', 'yes', 'on', '1', 1, True)

    FORMATTER_METHODS = {}

    def format_field(self, data, key, format, name=None, default=None):
        if name is None:
            name = key

        if key in data:
            if format == 'int':
                value = int(data[key])

            elif format == 'bool':
                value = data[key] in self.FORMATTER_TRUE_VALUES or data[key] not in self.FORMATTER_FALSE_VALUES

            elif format in self.FORMATTER_METHODS:
                value = self.FORMATTER_METHODS[format](data, key)

            #TODO: Control de formato no soportado/definido
            else:
                pass

        else:
            value = default

        data[name] = value


class BaseHandlerValidator(object):
    # Definir expresiones regulares para validar
    VALIDATION_REGEXP = {
        'amount': r'^[0-9]{10}$'
    }

    # Definir funciones para validar
    VALIDATION_METHOD = {}

    def validate_field(self, data, key, rule, strict=True):
        value = data[key] if key in data else None

        if (value is None or value == '') and not strict:
            return True

        if rule in self.VALIDATOR_REGEXP:
            return self.VALIDATOR_REGEXP[rule].match(value)

        elif rule in self.VALIDATION_METHOD:
            return self.VALIDATION_METHOD[rule](value)

        else:
            self.data_entry_validation_error(key, rule, strict)
            return False

    def add_validation_regexp(self, name, regexp):
        self.VALIDATION_REGEXP[name] = regexp

    def add_validation_method(self, name, method):
        self.VALIDATION_METHOD[name] = method


class BaseHandlerParser(object):
    def data_entry_process(self, mandatory, opcional, additional, rules, formats, params):
        data = {}

        # Obtención de parametros obligatorios y control de errores
        if not self.data_entry_mandatory(mandatory, data, params):
            return False

        # Obtención de parametros opcionales
        self.data_entry_optional(optional, data, params)

        # Obtención de parametros adicionales
        self.data_entry_additional(additional, data)

        # Comprobación de reglas de validación y control de errores
        if not self.data_entry_validate(rules, data):
            return False

        # Creación de campos calculados
        self.data_entry_format(formats, data)

        return data

    def data_entry_mandatory(self, keys, data, params):
        for key in keys:
            if key in params:
                data[key] = params[key]

            else:
                self.data_entry_mandatory_error(key)
                return False

        return True

    def data_entry_optional(self, items, data, params):
        for item in items:
            if isinstance(item, tuple):
                key, default = item

            else:
                key, default = (item, None)

            # Comprobar si viene en la petición
            if item in params:
                data[key] = params[key]

            else:
                data[key] = default

    def data_entry_additional(self, items, data):
        # Añadir campos adicionales a los parametros
        for key, value in items:
            data[key] = value


    def data_entry_validate(self, rules, data):
        for args in rules:
            if not self.validate_field(data, *args):
                return False

        return True

    def data_entry_format(self, formats, data):
        for args in formats:
            self.format_field(data, *args)
