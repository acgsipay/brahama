#!/usr/bin/python
# -*- coding: utf-8 -*-
from ..core.handlers import BaseHandler
from ..core.utils.collections import params

class MainHandler(HandlerBase):
    def post(self):
    # DATA ENTRY
    # ----------------------------------------------------------------

        # MANDATORY FIELDS
        # ------------------------------------------------------------
        # Comprueba que existan los parametros de entrada definido
        # en caso de no existir, se llamara a una función especifica
        # para registrar el suceso y devolver el mensaje adecuado.
        # ------------------------------------------------------------
        mandatory = ('mkey1', 'mkey2', 'mkey3')

        # OPTIONAL FIELDS
        # ------------------------------------------------------------
        # Obtiene parametros de entrada opcionales en caso de estar
        # presentes, en caso contrario, se puede definir el valor por
        # defecto
        # ------------------------------------------------------------
        optional = ('okey1', ('okey2', 'odefault1'), 'okey3')

        # ADDITIONAL FIELDS
        # ------------------------------------------------------------
        # Campos adicionales, obtenidos de las cabeceras o generados
        # ------------------------------------------------------------
        additional = (('akey1', 'avalue1'), ('akey2', 'avalue2'), ('akey3', 'avalue3'))

        # VALIDATIONS
        # ------------------------------------------------------------
        # Reglas de validación para los campos, se puede indicar que
        # hacer si el parametro no esta presente
        # ------------------------------------------------------------
        rules = (('mkey1', 'ramount'), ('okey2', 'rtext'), ('okey2', 'rdate', False))

        # FORMAT
        # ------------------------------------------------------------
        # Parametros calculados, con un parametro de entrada se puede
        # generar el valor de otro campo indicando la función de
        # formato, opcionalmente se puede indicar el nombre del
        # parametro, en caso contrario se sobreescribira el parametro
        # tambien, se puede para los parametros opcionales indicar un
        # valor por defecto
        # ------------------------------------------------------------
        formats = (('mkey1', 'fname1', 'ckey1'), ('okey2', 'fname2'), ('okey3', 'fname3', 'ckey3', 'fdefault3'))

        # PROCCESS DATA
        # ------------------------------------------------------------
        fields = self.data_entry_process(mandatory, optional, additional, rules, formats, self.params)

        # LOG DATA
        # ------------------------------------------------------------

        # El procesamiento de datos no a sido correcto, se a enviado al navegador
        if not fields:
            type = ''
            log_data_entry = {key: fields[key] for key in ('mkey1', 'mkey2', 'ckey1')}
            self.log_error(type='', code='', detail='Input Data Error', **log_data_entry)
            return

        else:
            log_data_entry = {key: fields[key] for key in ('mkey1', 'mkey2', 'ckey1')}
            self.log_info(type='', code='', detail='Input Data Success', **log_data_entry)


    # GET DATA PERSISTENCE
    # ------------------------------------------------------------
    # Obtener información de base de datos o memcache.
    # ------------------------------------------------------------

        # GET CACHE
        # ------------------------------------------------------------
        key = data['idrequest']
        cache = self.get_cache_data(key)


        # GET SOAP
        # ------------------------------------------------------------
        keys = ('mkey1', 'mkey2')
        args = parameterize(key, fields, cache)

        response = self.soap.get_environment(*args)

        if not response or not isinstance(response, dict) or not 'ResultCode' in response:
            protocol = 'soap'
            server = 'sipay_ecommerce'
            call = 'get_environment'
            self.server_not_response_error(protocol, server, call, args)
            return

        elif response['ResultCode'] != "0":



    # PROCESS DATA
    # ------------------------------------------------------------
    # Procesar la petición
    # ------------------------------------------------------------
        # GET SOAP
        # ------------------------------------------------------------
        keys = ('mkey1', 'mkey2')
        args = parameterize(key, fields, cache)
        cache = self.soap.get_environment(*args)
