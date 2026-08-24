import sys


def main() -> None:


    try:
        with open(sys.argv[1], "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()

                if not line or line.startswith("#"):
                    continue

                try:
                    if "=" not in line:
                        raise Exception("Equal sign is not found")

                    key, value = line.split("=", 1)

                    key = key.strip()
                    value = value.strip()

                    print(key, value)

                except Exception as e:
                    print(e)

    except FileNotFoundError:
        print("config.txt not found.")


main()
