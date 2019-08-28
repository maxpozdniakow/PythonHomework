import argparse


def main():
    parser = argparse.ArgumentParser(description='Pure-python command-line calculator.')
    parser.add_argument('EXPRESSION', type=str, help='expression string to evaluate')
    args = parser.parse_args()
    print(0)
