from enum import Enum


# Alert states that the user can set.
class AlertStateSetable(str, Enum):
    OPEN = "OPEN"
    IN_PROGRESS = "IN_PROGRESS"
    RISK_ACCEPTED = "RISK_ACCEPTED"
    MITIGATING_CONTROL = "MITIGATING_CONTROL"
    FALSE_POSITIVE = "FALSE_POSITIVE"


class OutputFormat(str, Enum):
    """
    Used to specify command-line parameters indicating output format.
    """

    JSON = "json"
    TABLE = "table"
    CSV = "csv"
    HTML = "html"


class AWSAccount(dict):
    """
    Class representing a AWS Account as returned by boto3
    """

    def __init__(self, Id: str, Name: str, Arn: str, Email: str, Onboard: bool = False):
        dict.__init__(self, Id=Id, Name=Name, Arn=Arn, Email=Email, Onboard=Onboard)
