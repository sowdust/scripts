# Example: python names_permutations.py -f firstname -l lastname

import sys
import argparse

parser = argparse.ArgumentParser(description='Name permutations to perform google search')
parser.add_argument('-f', '--firstname', metavar='firstname', type=str, help='First name')
parser.add_argument('-l', '--lastname', metavar='lastname', type=str, help='Last name')
parser.add_argument('-m', '--middlename', metavar='middlename', type=str, help='Middle name (optional)')

args = parser.parse_args(args=None if len(sys.argv) > 1 else ['--help'])

if not args.firstname or not args.lastname:
	print('[!] Error. First and last name are required. Exiting.')
	sys.exit(0)

firstname = args.firstname
lastname = args.lastname

search = []

search.append("%s %s" % (firstname,lastname))
search.append("\"%s %s\"" % (firstname,lastname))
search.append("\"\"%s\" \"%s\"\"" % (firstname,lastname))
search.append("%s, %s" % (lastname,firstname))
search.append("\"%s %s\"" % (lastname,firstname))
search.append("\"%s, %s\"" % (lastname,firstname))
search.append("%s. %s" % (firstname[0],lastname))
search.append("\"%s. %s\"" % (firstname[0],lastname))
search.append("%s. %s" % (lastname[0],firstname))
search.append("\"%s. %s\"" % (lastname[0],firstname))
search.append("inurl:%s%s" % (lastname,firstname))
search.append("inurl:%s%s" % (firstname,lastname))

if args.middlename is not None:
	middlename = args.middlename
	search.append("%s %s %s" % (firstname,middlename,lastname))
	search.append("%s %s. %s" % (firstname,middlename[0],lastname))
	search.append("\"%s %s. %s\"" % (firstname,middlename[0],lastname))
else:
	search.append("%s, %s *" % (lastname,firstname))
	search.append("\"%s * %s\"" % (firstname,lastname))

for s in search:
	print(s)

print()
print(' OR '.join(search))
