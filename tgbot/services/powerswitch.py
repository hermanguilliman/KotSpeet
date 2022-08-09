from dataclasses import dataclass
from enum import Enum
from subprocess import Popen
import platform

from loguru import logger


class Distros(Enum):
    linux = "Linux"
    windows = "Windows"
    darwin = "Darwin"


@dataclass
class BasicOperations:
    reboot: list[str]
    cancel: list[str]
    shutdown: list[str]


class LinuxOperations(BasicOperations):
    reboot = ["sudo", "reboot"]
    cancel = ["shutdown", "-c"]
    shutdown = ["shutdown", "-P", "0"]


class WindowsOperations(BasicOperations):
    reboot = ["shutdown", "/r", "/t", "0"]
    cancel = ["shutdown", "/a"]
    shutdown = ["shutdown", "/s", "/c", """ """, "/t", "1"]


class DarwinOperations(BasicOperations):
    reboot = ["sudo", "shutdown", "-r", "now"]
    cancel = ["sudo", "killall", "shutdown"]
    shutdown = ["sudo", "shutdown", "-h", "0"]


class DistroIsNotSupported(Exception):
    pass

class DistroIsNotDefined(Exception):
    pass


class PowerSwitcher:
    def __init__(self, distro=None):
        self.distro = distro
        if self.distro is None:
            self.distro = platform.system()
            if self.distro is None:
                DistroIsNotDefined
        elif self.distro == '':
            raise DistroIsNotSupported
        logger.debug(f"Current OS: {self.distro}")


    async def reboot(self):
        match self.distro:
            case Distros.linux.value:
                Popen(LinuxOperations.reboot)
            case Distros.windows.value:
                Popen(WindowsOperations.reboot)
            case Distros.darwin.value:
                Popen(DarwinOperations.reboot)
    
    async def shutdown(self):
        match self.distro:
            case Distros.linux.value:
                Popen(LinuxOperations.shutdown)
            case Distros.windows.value:
                Popen(WindowsOperations.shutdown)
            case Distros.darwin.value:
                Popen(DarwinOperations.shutdown)
