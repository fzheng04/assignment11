
import pytest
from pydantic import ValidationError

from app.schemas import CalculationCreate, CalculationRead


@pytest.mark.parametrize(
    "operation",
    ["add", "subtract", "multiply", "divide"],
)
def test_valid_operation_types(operation):
    data = CalculationCreate(a=10, b=5, type=operation)

    assert data.type.value == operation


def test_invalid_operation_type():
    with pytest.raises(ValidationError):
        CalculationCreate(a=10, b=5, type="power")


def test_division_by_zero():
    with pytest.raises(
        ValidationError, match="Cannot divide by zero"
    ):
        CalculationCreate(a=10, b=0, type="divide")


@pytest.mark.parametrize("missing_field", ["a", "b", "type"])
def test_missing_required_fields(missing_field):
    data = {"a": 10, "b": 5, "type": "add"}
    del data[missing_field]

    with pytest.raises(ValidationError):
        CalculationCreate(**data)


@pytest.mark.parametrize(
    "invalid_value",
    ["hello", None, [], {}],
)
def test_invalid_operand(invalid_value):
    with pytest.raises(ValidationError):
        CalculationCreate(a=invalid_value, b=5, type="add")


@pytest.mark.parametrize(
    "invalid_value",
    [float("nan"), float("inf"), float("-inf")],
)
def test_non_finite_numbers(invalid_value):
    with pytest.raises(ValidationError):
        CalculationCreate(a=invalid_value, b=5, type="add")


def test_calculation_read_serialization():
    calculation = CalculationRead(
        id=1,
        a=10,
        b=5,
        type="add",
        result=15,
    )

    output = calculation.model_dump(mode="json")

    assert output == {
        "id": 1,
        "a": 10.0,
        "b": 5.0,
        "type": "add",
        "result": 15.0,
    }
