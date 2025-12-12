class NoCoachAvailable(Exception):
    def __init__(self, message="No coach available") -> None:
        super().__init__(message)
