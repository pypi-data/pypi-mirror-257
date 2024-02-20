import sys
import json
from dotenv import dotenv_values
import pprint

from classes.ParserResult import ParserResult
from exceptions.NotDictException import NotDictException, is_dict
from exceptions.MethodNotValid import MethodNotValid, validate_method
from helpers.utils import class_to_json, json_to_dict
from rabbit.send_rabbit import send_message

RABBITMQ_EXCHANGE_PARSER_QUEUE = dotenv_values().get("RABBITMQ_EXCHANGE_PARSER_QUEUE")


def parser_result(parser_result_data):
    if isinstance(parser_result_data, str):
        parser_result_data = json_to_dict(parser_result_data)

    data_object = validate_parser_result(parser_result_data)

    method_to_execute = globals()[data_object.method]
    method_to_execute(data_object)


def validate_parser_result(parser_result: dict):
    try:
        # Validate that data provided is Dict
        is_dict(parser_result)
        # Validate that method provided exists
        validate_method(parser_result["Method"])

        return ParserResult(**parser_result)
    except ValueError as ve:
        print("Value Error: " + str(ve))
        sys.exit(1)
    except TypeError as te:
        print("Type Error: " + str(te))
        sys.exit(1)
    except NotDictException as nde:
        print("Dict Error: " + str(nde))
        sys.exit(1)
    except MethodNotValid as mnv:
        print("Method Error: " + str(mnv))
        sys.exit(1)


def validate_units(parser_result: ParserResult):
    data_converted = class_to_json(parser_result)
    # send_message(RABBITMQ_EXCHANGE_PARSER_QUEUE, data_converted, "validate_units")
    pprint.pprint(data_converted)
    print("validate_units")


def units_inspected(parser_result: ParserResult):
    data_converted = class_to_json(parser_result)
    # send_message(RABBITMQ_EXCHANGE_PARSER_QUEUE, data_converted, "units_inspected")
    pprint.pprint(data_converted)
    print("units_inspected")


def units_departed(parser_result: ParserResult):
    data_converted = class_to_json(parser_result)
    # send_message(RABBITMQ_EXCHANGE_PARSER_QUEUE, data_converted, "units_departed")
    pprint.pprint(data_converted)
    print("units_departed")


def state_change(parser_result: ParserResult):
    data_converted = class_to_json(parser_result)
    # send_message(RABBITMQ_EXCHANGE_PARSER_QUEUE, data_converted, "state_change")
    pprint.pprint(data_converted)
    print("state_change")


if __name__ == "__main__":
    parser_result(
        {
            "SerialNumber": "P69660003012311280100684",
            "Sequence": "None",
            "Assembly": "6966-0003-01",
            "RouteStep": "AOI_T",
            "WorkOrder": "None",
            "Step": "2",
            "Line": "L16",
            "IsPanel": True,
            "PassFail": 1,
            "User": "SAUL RUIZ",
            "StartTime": "2023-11-29T10:24:31",
            "EndTime": "2023-11-29T10:24:46",
            "MachineId": "AOI-L16",
            "ProgramName": "6966-0003-01_BOT",
            "LogFileName": "None",
            "Remarks": "None",
            "IsBirth": True,
            "Parameters": {"RecipeName": "6966-0003-01_BOT", "RecipeRevision": "None"},
            "TestResults": "None",
            "Method": "units_inspecteds",
            "ChildSerialNumbers": [
                {
                    "SerialNumber": "",
                    "Sequence": 1,
                    "TestResult": [
                        {
                            "TestName": "ST5901_Polarity3_Polarity_AI2-3D-1_AI2_3D_ConfidenceLevel",
                            "Sequence": 5,
                            "PassFail": "OK",
                            "LowLimit": "1",
                            "HighLimit": "100",
                            "Value": "82.3721508947464",
                            "IsCritical": True,
                            "Defect": "None",
                            "ErrorCode": "None",
                            "ErrorLocation": "None",
                            "ErrorMessage": "None",
                            "Parameters": "None",
                        },
                        {
                            "TestName": "ST5901_Polarity3_Polarity_AI2-3D-1_AI2_3D_ConfidenceLevel",
                            "Sequence": 5,
                            "PassFail": "OK",
                            "LowLimit": "1",
                            "HighLimit": "100",
                            "Value": "82.3721508947464",
                            "IsCritical": True,
                            "Defect": "None",
                            "ErrorCode": "None",
                            "ErrorLocation": "None",
                            "ErrorMessage": "None",
                            "Parameters": "None",
                        },
                    ],
                    "PassFail": 1,
                },
            ],
        }
    )
