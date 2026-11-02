from datetime import UTC, datetime, timedelta

from src.security import can_cancel


def test_owner_within_24h():
    now = datetime.now(UTC)
    assert can_cancel("NEW", 1, 1, False, now - timedelta(hours=1), now)

def test_stranger_denied():
    now = datetime.now(UTC)
    assert not can_cancel("NEW", 1, 2, False, now, now)

def test_shipped_denied_even_admin():
    now = datetime.now(UTC)
    assert not can_cancel("SHIPPED", 1, 1, True, now, now)

def test_expired_denied():
    now = datetime.now(UTC)
    assert not can_cancel("NEW", 1, 1, False, now - timedelta(hours=25), now)

# Nota: La función can_cancel ya debería estar importada al inicio del archivo original.

def test_admin_can_cancel_new_order_other_user():
    # Admin (is_admin=True) cancela pedido de otro (owner_id=1, user_id=2)
    now = datetime.now(UTC)
    assert can_cancel("NEW", 1, 2, True, now, now) == True

def test_owner_cannot_cancel_exactly_at_24_hours():
    # Dueño cancela a las 24 horas exactas (debe ser False)
    now = datetime.now(UTC)
    created = now - timedelta(hours=24)
    assert can_cancel("NEW", 1, 1, False, created, now) == False
