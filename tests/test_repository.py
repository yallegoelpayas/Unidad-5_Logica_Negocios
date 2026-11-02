from sqlalchemy import select
from sqlalchemy.orm import Session

from src.domain import Order
from src.repository import OrderRow, SqlOrderRepository, make_engine


def test_repository_commit():
    engine = make_engine()
    with Session(engine) as session:
        SqlOrderRepository(session).save(1, Order(120))
        session.commit()
        assert session.scalar(select(OrderRow).where(OrderRow.id == 1)).total == 120

def test_repository_rollback():
    engine = make_engine()
    with Session(engine) as session:
        SqlOrderRepository(session).save(1, Order(120))
        session.rollback()
        assert session.scalar(select(OrderRow).where(OrderRow.id == 1)) is None

def test_repository_save_250_id_2():
    engine = make_engine()
    with Session(engine) as session:
        # Arrange: Inicializar repositorio y pedido
        repo = SqlOrderRepository(session)
        order = Order(250)
        
        # Act: Guardar y hacer commit a la base de datos (pasando id y order)
        repo.save(2, order)
        session.commit()
        
        # Assert: Consultar la base de datos para verificar que se guardó correctamente
        saved = session.scalar(select(OrderRow).where(OrderRow.id == 2))
        assert saved.total == 250
        assert saved.status == "NEW"