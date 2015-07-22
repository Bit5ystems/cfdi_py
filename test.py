def testOnlyStamp():
    from itimbre.iTimbre import iTimbre
    
    handler = iTimbre(True) # Inicializado en modo debug
    handler.auth(handler.SERVICE_ONLY_STAMP, user='myUser', password='My_secured_pass', rfc='SAEH950225DU4')
    handler.onlyStampObject('<xml>', False)
    handler.postQuery()
    handler.handleResponse()


testOnlyStamp()

