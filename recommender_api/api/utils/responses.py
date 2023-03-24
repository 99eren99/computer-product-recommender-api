from flask import make_response,jsonify

def response_with(response, value=None, message=None, error=None,headers={}, pagination=None):
    result={}
    if value is not None:
        result.update(value)

    if message is not None:
        result.update({'message':message})

    result.update({'code':response["code"]})

    if error is not None:
        result.update({'error':error})
    
    if pagination is not None:
        result.update({'pagination':pagination})
    
    headers.update({"Access-Control-Allow-Origin":"*"})
    headers.update({"server":"Recommender App REST API"})

    return make_response(jsonify(result),response["http_code"],headers)

UNAUTHORIZED_403={
    "http_code":403,
    "code":"notAuthorized",
    "message":"You are not authorized to execute this."
}

SUCCESS_200={
    "http_code":200,
    "code":"success",
}

SUCCESS_201={
    "http_code":201,
    "code":"success",
}

SUCCESS_204={
    "http_code":204,
    "code":"success",
}