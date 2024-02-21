import argparse
import logging


def main():
    parser = argparse.ArgumentParser(
        prog="Docubot",
        description="Code document generator",
    )

    parser.add_argument("command", help="command to pick from (generate, update)")
    parser.add_argument("-l", "--log_level", default="info", help="Logging Level")
    parser.add_argument("-p", "--project", default=".", help="The project path")
    parser.add_argument(
        "-o",
        "--output",
        help="The output file path for the generated document",
    )
    args = parser.parse_args()

    if args.log_level.lower() in ["debug", "d"]:
        logging.basicConfig(level=logging.DEBUG)
    elif args.log_level.lower() in ["warn", "warning", "w"]:
        logging.basicConfig(level=logging.WARN)
    elif args.log_level.lower() in ["critical", "c"]:
        logging.basicConfig(level=logging.CRITICAL)
    elif args.log_level.lower() in ["fatal", "f"]:
        logging.basicConfig(level=logging.FATAL)
    else:
        logging.basicConfig(level=logging.INFO)

    logging.debug(f"arguments given: {args}")


if __name__ == "__main__":
    main()
