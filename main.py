if __name__ == "__main__":
    import sys
    args = sys.argv[1:]
    if len(args) != 1:
        print("This script requires exactly one command-line argument. Killing")
        exit(1)

    import Trading
    exit_code = Trading.run(args[0]) or 0
    exit(exit_code)
else:
    raise ImportError("Run this file directly, don't import it!")