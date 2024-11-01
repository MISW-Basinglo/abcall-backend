from src.common.constants import POLL_TIMEOUT
from src.daemon import EmailDaemon

if __name__ == "__main__":
    daemon = EmailDaemon(poll_interval=POLL_TIMEOUT)
    daemon.run()
