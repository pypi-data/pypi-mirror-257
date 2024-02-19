import ipih

from pih import A
from enum import IntEnum, auto
from pih.consts.hosts import Hosts
from BackupService.const import SD as BCK_SD
from pih.collections.service import ServiceDescription


NAME: str = "Automation"

HOST = Hosts.BACKUP_WORKER

VERSION: str = "1.11"

SD: ServiceDescription = ServiceDescription(
    name=NAME,
    description="Automation service",
    host=HOST.NAME,
    use_standalone=True,
    standalone_name="auto",
    version=VERSION,
)


class BACKUP_COMMANDS:
    ROOT_PATH: str = A.PTH.join(A.PTH_FCD.SERVICE_PATH(BCK_SD.name), "command")

    class ATTACH_SHARED_DISKS:

        FILE_NAME: str = "attach_shared_disks.ps1"

        @staticmethod
        def PATH() -> str:
            return A.PTH.join(
                BACKUP_COMMANDS.ROOT_PATH, BACKUP_COMMANDS.ATTACH_SHARED_DISKS.FILE_NAME
            )


class USER_LOGIN:
    SERVICE_CONTROL_HEAD: str = "aip"
    CHIEF_DOCTOR: str = "svm"
    LABARATORY_HEAD: str = "evl"


class ProblemState(IntEnum):
    AT_FIX = auto()
    WAIT_FOR_FIX_RESULT = auto()
    NOT_FIXED = auto()
    FIXED = auto()
