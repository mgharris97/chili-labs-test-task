
#JSend format for responses

def jsend_success(data):
    return{
        "status": "success",
        "data": data
    }

def jsend_fail(message):
    return{
        "status": "fail",
        "data": {"message": message}
    }

def jsen_error(message):
    return{
        "status": "error",
        "message": message
    }
