def success_response(data, message='Operación exitosa'):
    return {
        'success': True,
        'message': message,
        'data': data,
    }


def error_response(errors, message='Ocurrió un error'):
    return {
        'success': False,
        'message': message,
        'errors': errors,
    }
