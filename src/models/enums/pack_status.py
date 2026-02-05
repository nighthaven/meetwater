from enum import Enum


class PackStatus(Enum):
    PENDING = "PENDING"
    PAID = "PAID"
    USED = "USED"
    EXPIRED = "EXPIRED"
