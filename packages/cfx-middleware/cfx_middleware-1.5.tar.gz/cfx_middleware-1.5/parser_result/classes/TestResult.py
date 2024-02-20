class TestResult:
    def __init__(
        self,
        TestName,
        Sequence,
        PassFail,
        LowLimit,
        HighLimit,
        Value,
        IsCritical,
        Defect,
        ErrorCode,
        ErrorLocation,
        ErrorMessage,
        Parameters,
    ):
        if not isinstance(IsCritical, bool):
            raise ValueError("IsCritical must be Boolean")

        if not isinstance(Sequence, int):
            raise ValueError("Sequence must be integer")

        self.test_name = TestName
        self.sequence = Sequence
        self.pass_fail = PassFail
        self.low_limit = LowLimit
        self.high_limit = HighLimit
        self.value = Value
        self.is_critical = IsCritical
        self.defect = Defect
        self.error_code = ErrorCode
        self.error_location = ErrorLocation
        self.error_message = ErrorMessage
        self.parameters = Parameters

    def to_dict(self):
        return vars(self)
