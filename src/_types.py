from enum import Enum


class OrderStatus(Enum):
    IN_PROGRESS = 0
    SHIPPED = 1
    DELIVERED = 2
