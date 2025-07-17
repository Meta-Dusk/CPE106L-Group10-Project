import re
import inspect
import os

def is_valid_hex_color(code: str) -> bool:
    return isinstance(code, str) and re.fullmatch(r"#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})", code) is not None

def where_am_i(stack: int = 1):
    frame = inspect.stack()[stack]  # [0] is current function, [1] is caller
    caller_file = frame.filename  # full path to calling file
    return os.path.basename(caller_file)  # just the filename

def get_caller_script():
    for frame_info in inspect.stack():
        filename = os.path.basename(frame_info.filename)
        if filename != os.path.basename(__file__):
            return filename
    return "Unknown"

def print_call_chain():
    print("🔗 Call Chain:")
    stack = inspect.stack()
    for i, frame_info in enumerate(stack[1:]):  # skip this function's own frame
        filename = os.path.basename(frame_info.filename)
        lineno = frame_info.lineno
        func = frame_info.function
        print(f"  {i + 1}. {filename}:{lineno} — {func}()")

def test():
    print(f"Called from: {where_am_i()}")
    
if __name__ == "__main__":
    test()