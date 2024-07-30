def greeting(names):
    hello_str = "Hello "
    output = ""
    for name in ["Alice", "Bob"]:
        output += f"{hello_str}{name}\n"
    if isinstance(names, str):
        output += f"{hello_str}{names}\n"
    return output
