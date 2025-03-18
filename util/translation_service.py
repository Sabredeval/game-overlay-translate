import subprocess
import threading
import time
import os
import sys
import requests
import platform
import signal
import atexit

class LibreTranslateService:
    """Manages a local LibreTranslate service instance"""
    
    def __init__(self, host="127.0.0.1", port=5000):
        self.host = host
        self.port = port
        self.url = f"http://{host}:{port}"
        self.api_url = f"{self.url}/translate"
        self.process = None
        self.ready = False
        self._startup_thread = None
        
    def start(self):
        """Start the LibreTranslate service in background"""
        if self.is_running():
            print("LibreTranslate service is already running")
            self.ready = True
            return True
            
        def _run_service():
            print("Starting LibreTranslate service...")
            
            # Determine if running from frozen exe or script
            if getattr(sys, 'frozen', False):
                # If frozen (e.g., PyInstaller), use sys._MEIPASS
                base_dir = getattr(sys, '_MEIPASS', os.path.dirname(sys.executable))
            else:
                # If running as script, use current directory
                base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            
            # Prepare command with appropriate settings
            cmd = [
                sys.executable, "-m", "libretranslate", 
                "--host", self.host,
                "--port", str(self.port),
                "--load-only", "en,es,fr,de",  # Load only needed languages to save memory
                "--disable-files-translation",  # For security
                "--debug",  # More verbose output for troubleshooting
            ]
            
            startupinfo = None
            if platform.system() == "Windows":
                # Hide console window on Windows
                startupinfo = subprocess.STARTUPINFO()
                startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                startupinfo.wShowWindow = 0  # SW_HIDE
            
            try:
                # Start the process
                self.process = subprocess.Popen(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    startupinfo=startupinfo
                )
                
                # Register cleanup handler
                atexit.register(self.stop)
                
                # Wait for service to be ready
                max_attempts = 30  # Wait up to 30 seconds
                attempt = 0
                
                while attempt < max_attempts:
                    try:
                        response = requests.get(f"{self.url}/languages")
                        if response.status_code == 200:
                            print("LibreTranslate service is ready")
                            self.ready = True
                            break
                    except requests.exceptions.RequestException:
                        pass
                    
                    time.sleep(1)
                    attempt += 1
                
                if not self.ready:
                    print("Failed to start LibreTranslate service in time")
                    self.stop()
                    return False
                    
                return True
                
            except Exception as e:
                print(f"Error starting LibreTranslate service: {e}")
                self.process = None
                return False
        
        # Start the service in a separate thread
        self._startup_thread = threading.Thread(target=_run_service, daemon=True)
        self._startup_thread.start()
        
        # Return immediately, the service will be initialized in the background
        return True
    
    def stop(self):
        """Stop the LibreTranslate service"""
        if self.process:
            print("Stopping LibreTranslate service...")
            try:
                if platform.system() == "Windows":
                    # Windows requires different process termination approach
                    self.process.terminate()
                else:
                    # On Unix, we can use the process group
                    os.killpg(os.getpgid(self.process.pid), signal.SIGTERM)
            except Exception as e:
                print(f"Error stopping LibreTranslate service: {e}")
            finally:
                self.process = None
                self.ready = False
    
    def is_running(self):
        """Check if LibreTranslate service is already running"""
        if self.process:
            return self.process.poll() is None
            
        # Try to connect to the service
        try:
            response = requests.get(f"{self.url}/languages", timeout=2)
            return response.status_code == 200
        except:
            return False
    
    def wait_until_ready(self, timeout=30):
        """Wait until the service is ready or timeout occurs"""
        if self.ready:
            return True
            
        start_time = time.time()
        while time.time() - start_time < timeout:
            if self.ready:
                return True
            time.sleep(0.5)
        
        return False
    
    def translate(self, text, source="en", target="es"):
        """Translate text using the LibreTranslate service"""
        if not self.is_running():
            print("Translation service is not running")
            return None
            
        try:
            response = requests.post(
                self.api_url,
                json={
                    "q": text,
                    "source": source,
                    "target": target,
                    "format": "text"
                },
                timeout=5
            )
            
            if response.status_code == 200:
                result = response.json()
                return result.get("translatedText")
            else:
                print(f"Translation failed with status {response.status_code}")
                print(response.text)
                return None
                
        except Exception as e:
            print(f"Translation error: {e}")
            return None