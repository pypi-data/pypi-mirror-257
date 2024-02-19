import ipih

from pih.collections.service import ServiceDescription
from pih.consts.hosts import Hosts

NAME: str = "MessageReceiver"

HOST = Hosts.BACKUP_WORKER

VERSION: str = "1.21"

PACKAGES: tuple[str, ...] = ("fastapi", "uvicorn")

SD: ServiceDescription = ServiceDescription(
    name=NAME,
    description="Message receiver service",
    host=HOST.NAME,
    host_changeable=False,
    version=VERSION,
    standalone_name="msg_rcv",
    use_standalone=True,
    packages=PACKAGES
)
