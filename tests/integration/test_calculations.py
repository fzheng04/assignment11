
import pytest
from pydantic import ValidationError
from sqlalchemy import select

from app.database import SessionLocal
from app.models import Calculation
from app.schemas import CalculationCreate, CalculationRead
from app.calculation_factory import CalculationFactory


@pytest.fixture
def db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.mark.parametrize(
    "operation,a,b,expected",
    [
        ("add", 10, 5, 15),
        ("subtract", 10, 5, 5),
        ("multiply", 10, 5, 50),
        ("divide", 10, 5, 2),
    ],
)
def test_save_and_retrieve_calculation(
    db_session, operation, a, b, expected
):
    data = CalculationCreate(a=a, b=b, type=operation)
    calculation = CalculationFactory.create(data)

    record_id = None

    try:
        db_session.add(calculation)
        db_session.commit()
        db_session.refresh(calculation)

        record_id = calculation.id
        assert record_id is not None

        db_session.expunge_all()

        stored = db_session.scalar(
            select(Calculation).where(
                Calculation.id == record_id
            )
        )

        assert stored is not None
        assert stored.a == a
        assert stored.b == b
        assert stored.type == operation
        assert stored.result == pytest.approx(expected)

        response = CalculationRead.model_validate(stored)
        assert response.result == pytest.approx(expected)

    finally:
        db_session.rollback()

        if record_id is not None:
            saved = db_session.get(Calculation, record_id)
            if saved is not None:
                db_session.delete(saved)
                db_session.commit()


def test_invalid_operation_not_saved(db_session):
    with pytest.raises(ValidationError):
        CalculationCreate(a=10, b=5, type="invalid")


def test_division_by_zero_not_saved(db_session):
    with pytest.raises(ValidationError):
        CalculationCreate(a=10, b=0, type="divide")
