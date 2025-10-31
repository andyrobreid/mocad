def main():
    print("""
Hello, This repository aims to provide tooling for codecad workflows using marimo notebooks.

Have a look at the example `./examples/codecad-nb.py` to start.

To run in notebook edit form and iterate on the design:
    `uv run marimo edit`

To run in script form and get model output: 
    `uv run ./examples/codecad-nb.py --help`
    """)


if __name__ == "__main__":
    main()
