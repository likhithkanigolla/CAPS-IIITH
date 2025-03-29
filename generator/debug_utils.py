import traceback

# Enable debug mode - set to True for detailed debug output
DEBUG = True

def debug_print(message):
    """Print debug messages when DEBUG is enabled"""
    if DEBUG:
        print(f"[DEBUG] {message}")

def log_exception(e):
    """Log exception details when DEBUG is enabled"""
    if DEBUG:
        print(f"[DEBUG] Exception: {str(e)}")
        print(f"[DEBUG] Traceback: {traceback.format_exc()}")
