"""Script with arguments to """


import argparse
import sys
import ogr_rust as ogr

def main():

    parser = argparse.ArgumentParser(prog='OGR')
    subparsers = parser.add_subparsers()

    parser_enum = subparsers.add_parser('enum', help="Enumerate rulers")
    parser_enum.add_argument('length', type=int, help="The max length of the Ruler")
    parser_enum.add_argument('--subcommand', default='enum', help=argparse.SUPPRESS)
    parser_enum.add_argument('-o', '--order', type=int, default=None, help="Restrict the order of our rulers")
    parser_enum.add_argument('-g', '--golomb', action='store_true', help="Keep only golomb rulers")
    parser_enum.add_argument('-x', '--exact', action='store_true', help="Only print rulers whose length matches `length` exactly")

    parser_search = subparsers.add_parser('search', help="Look for an optimal ruler")
    parser_search.add_argument('order', type=int, help='The order of the ruler to search for')
    parser_search.add_argument('--subcommand', default='search', help=argparse.SUPPRESS)

    parser_rand = subparsers.add_parser('rand', help="Generate random rulers")
    parser_rand.add_argument('length', type=int, help='The length of the ruler')
    parser_rand.add_argument('-n', '--trials', type=int, default=1, help='The number of rulers to return. Default 1')
    parser_rand.add_argument('--subcommand', default='rand', help=argparse.SUPPRESS)


    # Draw random rulers until we get one with the golomb property!
    parser_draw = subparsers.add_parser('draw', help="Randomly draw rulers until we get one with the golomb property")
    parser_draw.add_argument('length', type=int)
    parser_draw.add_argument('--subcommand', default='draw', help=argparse.SUPPRESS)

    parser_list = subparsers.add_parser('ls', help="Print the first n rulers")
    parser_list.add_argument('n', type=int)
    parser_list.add_argument('--subcommand', default='ls', help=argparse.SUPPRESS)
    parser_list.add_argument('--from', type=int, dest="start", default=0)
    parser_list.add_argument('--state', action="store_true")



    args = parser.parse_args()

    try:
        if args.subcommand is None:
            pass
    except:
        parser.print_help()
        exit(1)

    if args.subcommand == 'enum':
        print("Executing enum!")
        rulers = ogr.enumerate_rulers(args.length)

        if args.golomb:
            rulers = [r for r in rulers if r.is_golomb_ruler()]

        if args.order is not None:
            rulers = [r for r in rulers if r.order() == args.order]

        if args.exact:
            rulers = [r for r in rulers if r.length() == args.length]

        for r in rulers:
            print(r)

        if args.golomb and args.order:
            print(f"{len(rulers)} golomb rulers with order {args.order} and max length {args.length}")
        else:
            print(f"{len(rulers)} rulers")

    elif args.subcommand == 'search':
        print("Searching!!")

        # We want to iterate non stop until we've found a ruler
        for i in range(10):
            print(i, ogr.Ruler.from_id(i))


    elif args.subcommand == 'rand':

        print("Rand!")
        for _ in range(args.trials):
            print(get_random_ruler_length(args.length))

    elif args.subcommand == 'draw':

        count = 0
        draw = get_random_ruler_length(args.length)

        while not draw.is_golomb_ruler():
            count += 1
            draw = get_random_ruler_length(args.length)

        print(count, draw)

    elif args.subcommand == 'ls':

        print("  Id")
        print(f"-------")
        for i in range(args.start, args.start + args.n):
            if args.state:
                r = ogr.Ruler.from_id(i)
                print(f"[{i:5}] {str(r)[:20]}\t{r.to_state()}")
            else:
                print(f"[{i:5}] {ogr.Ruler.from_id(i)}")



# ---------------------------------------------------------------------------- #
#                                 Library code                                 #
# ---------------------------------------------------------------------------- #
# Functions to get some random rulers
# What's the number to length calculation?
import math
import random

"""Return the id range of rulers with length `length`."""
def range_ruler_length(length: int) -> tuple[int, int]:
    if length == 0: return (0, 0)
    elif length == 1: return (1, 1)
    else: return (2 ** (length - 1), (2 ** length) - 1)

def get_random_ruler_length(length: int):
    range = range_ruler_length(length)
    return ogr.Ruler.from_id(random.randint(range[0], range[1]))

def erdos_turan(odd_prime: int) -> list[int]:
    return [2 * odd_prime * k + ((k * k) % odd_prime) for k in range(0, odd_prime)]


if __name__ == '__main__':
    main()


    et = erdos_turan(37)
    print(et)