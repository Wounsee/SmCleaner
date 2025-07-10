import ctypes
import sys
from engine.ui import ConsoleInterface
if not ctypes.windll.shell32.IsUserAnAdmin():
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
    sys.exit()
if __name__ == "__main__":
    app = ConsoleInterface()
    app.run()