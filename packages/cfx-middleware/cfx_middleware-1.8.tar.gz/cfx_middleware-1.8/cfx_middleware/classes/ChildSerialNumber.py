from cfx_middleware.classes.TestResult import TestResult as C_TestResult


class ChildSerialNumber:
    def __init__(
        self,
        SerialNumber,
        Sequence,
        TestResult,
        PassFail,
    ):
        if not isinstance(Sequence, int):
            raise ValueError("Sequence must be integer")

        self.serial_number = SerialNumber
        self.sequence = Sequence
        self.test_result = [C_TestResult(**tr) for tr in TestResult]
        self.pass_fail = PassFail

    def to_dict(self):
        return vars(self)
