import argparse


def main():
    return 0


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Pure-python command-line calculator.')
    parser.add_argument('EXPRESSION', type=str,
                        help='expression string to evaluate')
    args = parser.parse_args()
    print(main())
