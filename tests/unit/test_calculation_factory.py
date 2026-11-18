
import pytest

from app.calculation_factory import CalculationFactory
from app.models import Calculation
from app.schemas import CalculationCreate, CalculationRead


@pytest.mark.parametrize(
    "operation,a,b,expected",
    [
        ("add", 10, 5, 15),
        ("subtract", 10, 5, 5),
        ("multiply", 10, 5, 50),
        ("divide", 10, 5, 2),
        ("add", -5, 3, -2),
        ("multiply", 0, 10, 0),
        ("divide", 5, 2, 2.5),
    ],
)
def test_factory_operations(operation, a, b, expected):
    data = CalculationCreate(a=a, b=b, type=operation)

    calculation = CalculationFactory.create(data)

    assert isinstance(calculation, Calculation)
    assert calculation.a == a
    assert calculation.b == b
    assert calculation.type == operation
    assert calculation.result == pytest.approx(expected)


def test_factory_does_not_save_automatically():
    data = CalculationCreate(a=5, b=3, type="add")

    calculation = CalculationFactory.create(data)

    assert calculation.id is None
    assert calculation.result == 8


def test_calculation_read():
    data = CalculationCreate(a=10, b=5, type="divide")
    calculation = CalculationFactory.create(data)
    calculation.id = 1

    response = CalculationRead.model_validate(calculation)

    assert response.id == 1
    assert response.a == 10
    assert response.b == 5
    assert response.type.value == "divide"
    assert response.result == 2
    assert "password_hash" not in response.model_dump()
