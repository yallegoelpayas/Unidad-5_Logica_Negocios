from unittest.mock import Mock

import pytest

from src.application import OrderService
from src.domain import Order


def test_gateway_approved():
    gateway = Mock()
    gateway.charge.return_value = True
    assert OrderService(gateway).checkout(Order(100)) == 100
    gateway.charge.assert_called_once_with(100)

def test_gateway_rejected():
    gateway = Mock()
    gateway.charge.return_value = False
    with pytest.raises(RuntimeError):
        OrderService(gateway).checkout(Order(100))
def test_payment_rejected_vip_200():
    # Arrange: Creamos el mock y forzamos a que rechace el pago (False)
    gateway = Mock()
    gateway.charge.return_value = False 
    
    # Preparamos el pedido VIP de 200 (con descuento debe quedar en 170)
    order = Order(200, vip=True)
    service = OrderService(gateway)
    
    # Act & Assert: Verificamos que lance el error de rechazo
    with pytest.raises(RuntimeError, match="payment rejected"):
        service.checkout(order)
    
    # Verificamos que el sistema intentó cobrar exactamente 170
    gateway.charge.assert_called_once_with(170)