# Generates a JSON trace that is compatible with the js/pytutor.ts frontend

import json
import sys
from optparse import OptionParser
from .json_tracer import JSONTracer, preload_imports

# To make regression tests work consistently across platforms,
# standardize display of floats to 3 significant figures
#
# Trick from:
# http://stackoverflow.com/questions/1447287/format-floats-with-standard-json-module
json.encoder.FLOAT_REPR = lambda f: ('%.3f' % f)


parser = OptionParser(usage="Generate JSON trace for pytutor")
parser.add_option('-p', '--heapPrimitives', default=False, action='store_true',
                  help='render primitives as heap objects.')
parser.add_option('--allmodules', default=False, action='store_true',
                  help='allow importing of all installed Python modules.')
parser.add_option("--code", dest="usercode", default=None,
                  help="Load user code from a string instead of a file and output compact JSON")

(options, args) = parser.parse_args()

code = None
if options.usercode:
    code = options.usercode
else:
    fin = sys.stdin if args[0] == "-" else open(args[0])
    code = fin.read()

if options.allmodules:
    preload_imports(code)

print(JSONTracer(options.heapPrimitives).runscript(code))
