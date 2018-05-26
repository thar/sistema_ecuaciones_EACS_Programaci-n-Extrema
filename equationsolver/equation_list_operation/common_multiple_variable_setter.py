from equationsolver.equation import Side, Equation
from equationsolver.equation_list_operation.equation_list_operation import EquationListOperation
from equationsolver.equation_list_operation.equation_list_operation_applier import EquationListOperationApplier


class CommonMultipleVariableSetter(EquationListOperation):
    def __init__(self, variable_name):
        EquationListOperation.__init__(self)
        self._variable_name = variable_name
        self._variable_values = []
        self._multiplication_values = []
        self._common_multiple = 1.0

    def apply(self):
        self._normalize()
        self._get_variable_values()
        self._get_common_multiple()
        self._get_multiplication_value_list()
        self._apply_multiplication_values()

    def _normalize(self):
        normalizer = EquationListOperationApplier(Equation.Normalizer())
        normalizer.set_equation_list(self._equation_list)
        normalizer.apply()

    def _get_variable_values(self):
        self._variable_values = []
        for eq in self._equation_list:
            self._variable_values.append(eq.get_value_variable(Side.left, self._variable_name))

    def _get_common_multiple(self):
        self._common_multiple = 1.0
        for value in self._variable_values:
            if value != 0:
                self._common_multiple *= value
        self._common_multiple = abs(self._common_multiple)

    def _get_multiplication_value_list(self):
        self._multiplication_values = []
        for i in range(len(self._variable_values)):
            value = self._variable_values[i]
            if value != 0:
                self._multiplication_values.append(self._common_multiple / value)
            else:
                self._multiplication_values.append(1.0)

    def _apply_multiplication_values(self):
        for i in range(len(self._equation_list)):
            self._equation_list[i].apply_operation(Equation.ValueMultiplier(self._multiplication_values[i]))
