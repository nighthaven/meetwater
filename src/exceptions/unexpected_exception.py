from fastapi import HTTPException, status

class UnexpectedException(HTTPException):
    def __init__(self, detail: str = "Une erreur inattendue est survenue."):
        super().__init__(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=detail)