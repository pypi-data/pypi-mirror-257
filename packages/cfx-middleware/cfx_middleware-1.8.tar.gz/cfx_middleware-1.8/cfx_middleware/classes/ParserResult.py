from cfx_middleware.classes.Parameters import Parameters as C_Parameters
from cfx_middleware.classes.ChildSerialNumber import ChildSerialNumber


class ParserResult:
    def __init__(
        self,
        Method,
        SerialNumber,
        Sequence,
        Assembly,
        RouteStep,
        WorkOrder,
        Step,
        Line,
        IsPanel,
        PassFail,
        User,
        StartTime,
        EndTime,
        MachineId,
        ProgramName,
        LogFileName,
        Remarks,
        IsBirth,
        Parameters,
        TestResults,
        ChildSerialNumbers,
    ):
        if not isinstance(IsPanel, bool):
            raise ValueError("IsPanel must be Boolean")

        if not isinstance(IsBirth, bool):
            raise ValueError("IsBirth must be Boolean")

        self.method = Method
        self.serial_number = SerialNumber
        self.sequence = Sequence
        self.assembly = Assembly
        self.route_step = RouteStep
        self.work_order = WorkOrder
        self.step = Step
        self.line = Line
        self.is_panel = IsPanel
        self.pass_fail = PassFail
        self.user = User
        self.start_time = StartTime
        self.end_time = EndTime
        self.machine_id = MachineId
        self.program_name = ProgramName
        self.log_file_name = LogFileName
        self.remarks = Remarks
        self.is_birth = IsBirth
        self.parameters = C_Parameters(**Parameters)
        self.test_results = TestResults
        self.child_serial_numbers = [
            ChildSerialNumber(**csn) for csn in ChildSerialNumbers
        ]
