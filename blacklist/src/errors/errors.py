class ApiError(Exception):
    code = 422
    description = "Default message"

class NotToken(ApiError):
    code = 403
    description = "El token no está en el encabezado de la solicitud."

class TokenInvalid(ApiError):
    code = 401
    description = "El token no es válido o está vencido."

class NotFound(ApiError):
    code = 400
    description = "Faltan campos en la solicitud"

class BadRequest(ApiError):
    code = 412
    description = "La información suministrada es erronea"

class EmailExist(ApiError):
    code = 409
    description = 'El email ya se encuentra en la lista negra'
    
class TokenDontExist(ApiError):
    code = 403
    
class TokenInvalid(ApiError):
    code = 401

class NotFoundPost(ApiError):
    code = 404
