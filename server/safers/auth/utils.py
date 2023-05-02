def reshape_auth_errors(error_response):
    """
    Reshapes errors from FusionAuth into a format suitable for DRF
    """
    return {
        field: [error.get("message") for error in errors]
        for field,
        errors in error_response.get("fieldErrors", {}).items()
    }
