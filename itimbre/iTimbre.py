import json

class iTimbre:

    service = None
    credentials = dict()
    testing = object;
    debug = False
    urlTarget = object
    request = object
    sandbox = False

    def __init__(self, debug=False, sanbox=False):
        self.debug = debug
        self.sandbox = sanbox
        msg = ''
        if debug:
            msg += 'Modo debug activado.\n'
        if sanbox:
            msg += 'Apuntando a Sandbox\n'


        self.reporter('Inicializando objeto iTimbre\n' + str(msg))

        return

    def auth(self, service=None, user='administrador', password='Administr4dor', account='demo', testing=False, rfc=None):
        self.testing = testing
        msg = ''

        if testing:
            msg += 'Utilizando servicio de pruebas.\n'

        if service == self.SERVICE_IFACTURA_SERVICE:
            self.credentials = self.createiFacturaCredentials(user, password, account)

            if self.testing and self.sandbox:
                self.urlTarget = self.URL_IFACTURA_SERVICE_SANDBOX
                msg += 'Apuntando al servicio de iFactura en Sanbox.\n'
            else:
                self.urlTarget = self.URL_IFACTURA_SERVICE
                msg += 'Apuntando al servicio de iFactura.\n'

        elif service == self.SERVICE_ONLY_STAMP:
            self.credentials = self.onlyStampCredentials(user, password, account, rfc)
            if self.testing:
                self.urlTarget = self.URL_ONLY_STAMP_TESTING
                msg += 'Apuntando al servicio de solo timbrado.\n'
            else:
                self.urlTarget = self.URL_ONLY_STAMP
                msg += 'Apuntando al servicio de solo timbrado en pruebas.\n'

        msg += 'Se han generado las credenciales: ' + json.dumps(self.credentials) + ' \n'
        self.reporter(msg)
        return

    def createiFacturaCredentials(self, user=None, password=None, account=None):
        return {
               self.PARAM_IFACTURA_ACCOUNT_LABEL: account,
               self.PARAM__USER_LABEL: user,
               self.PARAM_IFACTURA_PASS_LABEL: password,
               }

    def onlyStampCredentials(self, user=None, password=None, account=None, rfc=None,):
        return {
               self.PARAM__USER_LABEL: user,
               self.PARAM_ONLY_STAMP_PASS_LABEL: password,
               self.PARAM_ONLY_STAMP_RFC: rfc
               }


    def onlyStampObject(self, xml=None, isPayroll=None):
        if isPayroll:
            method = self.METHOD_STAMP_PAYROLL
        else:
            method = self.METHOD_STAMP_INVOICE

        params = dict()
        params = self.credentials.copy()
        params.update({self.PARAM_ONLY_STAMP_XML:xml})

        self.query = {
                      self.PARAM_METHOD : method,
                      self.PARAMS_LABEL : params
                      }

        self.reporter('Preparado para enviar: ' + json.dumps(self.query) + '\n')
        return

    def postQuery(self):
        import requests
        self.reporter('Se enviara el query a: ' + self.urlTarget)
        self.request = requests.post(url='https://' + self.urlTarget, data={self.CONTRACT_CONTAINER:json.dumps(self.query)})
        self.reporter('\nSe ha recibido: ' + str(self.request.json()) + '\n')
        return


    def reporter(self, msg=''):
        if self.debug:
            return print(str(msg) + '\n')
        return False




    # CONSTANTS

    SERVICE_ONLY_STAMP = 'solo-timrado'
    SERVICE_IFACTURA_SERVICE = 'iFactura'

    PARAM__USER_LABEL = 'user'
    PARAM_IFACTURA_PASS_LABEL = 'password'
    PARAM_IFACTURA_ACCOUNT_LABEL = 'cuenta'

    PARAM_ONLY_STAMP_PASS_LABEL = 'pass'
    PARAM_ONLY_STAMP_RFC = 'RFC'
    PARAM_ONLY_STAMP_XML = 'xmldata'
    PARAM_METHOD = 'method'

    PARAMS_LABEL = 'params'

    METHOD_STAMP_INVOICE = 'cfd2cfdi'
    METHOD_STAMP_PAYROLL = 'nomina2cfdi'

    METHOD_IFACTURA_INVOICE = 'nueva_factura'
    METHOD_IFACTURA_RECEIPT = 'nuevo_recibo'

    CONTRACT_CONTAINER = 'q'

    URL_ONLY_STAMP = 'portalws.itimbre.com/itimbre.php'
    URL_ONLY_STAMP_TESTING = 'portalws.itimbre.com/itimbreprueba.php'

    URL_IFACTURA_SERVICE = 'facturacion.itimbre.com/service.php'

#   Sandbox es la versión BETA de iFactura, no se garantiza su correcto funcionamiento.
    URL_IFACTURA_SERVICE_SANDBOX = 'sandbox.itimbre.com/service.php'








