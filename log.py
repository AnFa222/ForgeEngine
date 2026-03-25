def error(message):
    print(f"[ERROR] {message}")
    with open("error.log", "a") as f:
        f.write(f"[ERROR] {message}\n")