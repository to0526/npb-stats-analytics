import sys
import time
import threading

class Spinner:
    def __init__(self, message="考え中"):
        self.message = message
        self._running = False
        self._thread = None

    def start(self):
        self._running = True
        self._thread = threading.Thread(target=self._spin)
        self._thread.start()

    def stop(self):
        self._running = False
        if self._thread:
            self._thread.join()
        # 行を消す
        sys.stdout.write("\r" + " " * 40 + "\r")
        sys.stdout.flush()

    def _spin(self):
        chars = "|/-\\"
        idx = 0
        while self._running:
            sys.stdout.write(
                f"\r{self.message}… {chars[idx % len(chars)]}"
            )
            sys.stdout.flush()
            idx += 1
            time.sleep(0.1)
