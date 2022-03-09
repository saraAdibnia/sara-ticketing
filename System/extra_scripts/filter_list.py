def get_filters(allowed_filters:iter,request) -> dict:
    kwargs = {}
    for key, value in request.query_params.items():
        if key in allowed_filters:
            kwargs.update({key: value})
    return kwargs
