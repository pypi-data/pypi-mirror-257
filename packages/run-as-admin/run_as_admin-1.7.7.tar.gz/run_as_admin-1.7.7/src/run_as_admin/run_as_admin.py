import ctypes,os,logging

class RunAsAdmin:
    _run_file_path = None
    _is_log = True
    _log_file = None

    def __init__(self, FilePath, logging=False,log_file_path = os.path.join(os.getcwd(), "execution_log.log")):
        self._run_file_path = os.path.abspath(FilePath)
        self._is_log = logging
        self._log_file = os.path.abspath(log_file_path)

    def execute(self):
        try:
            hinstance = ctypes.windll.shell32.ShellExecuteW(None, "runas", self._run_file_path, None, None, 1)
            if hinstance <= 32:
                if self._is_log:
                    logging.basicConfig(filename=self._log_file, level=logging.DEBUG)
                    logging.error(f"Failed to execute with admin privileges. Return code: {hinstance}")
            else:
                if self._is_log:
                    logging.basicConfig(filename=self._log_file, level=logging.DEBUG)
                    logging.info("Successfully executed with admin privileges.")
        except Exception as e:
            if self._is_log:
                logging.basicConfig(filename=self._log_file, level=logging.DEBUG)
            return False
        return True

# Example usage
if __name__ == "__main__":
    pass