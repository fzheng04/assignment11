
from app.operations import add, subtract, multiply, divide
from app.schemas import CalculationCreate, CalculationType
from app.models import Calculation


class CalculationFactory:
    OPERATIONS = {
        CalculationType.ADD: add,
        CalculationType.SUBTRACT: subtract,
        CalculationType.MULTIPLY: multiply,
        CalculationType.DIVIDE: divide,
    }

    @classmethod
    def create(cls, data: CalculationCreate) -> Calculation:
        operation = cls.OPERATIONS[data.type]

        result = operation(data.a, data.b)

        return Calculation(
            a=data.a,
            b=data.b,
            type=data.type.value,
            result=result,
        )
