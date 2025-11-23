from enum import Enum


class BookingStatus(str, Enum):
    ACCEPTED = "ACCEPTED"
    PASSED = "PASSED"
    CANCELLED = "CANCELLED"
