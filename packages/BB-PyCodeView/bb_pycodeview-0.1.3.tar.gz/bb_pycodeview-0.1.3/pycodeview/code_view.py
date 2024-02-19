import sys, os, re, builtins, operator

try:
    from bblogger import getLogger
    log = getLogger(__name__)
    if log.level == 1:
        log.set_format('debug')

    from texttools import FG as c, Styles as S, Ansi, AnsiList
    from apputils import Path

except ImportError:
    print("Please install 'bb_apputils' >= v0.5.0 to use this script")
    if __name__ == "__main__":
        sys.exit(1)

except Exception as E:
    print(str(E))
    if __name__ == "__main__":
        sys.exit(1)

from importlib import import_module as imp
from importlib.resources import files as _src
from .syntax_highlighter import SyntaxHighlighter, CODE_BACKGROUND
from . import __version__

from . import _data
HTML_TEMPLATE = _src(_data).joinpath( 'template.html' )
DATA_DIR = Path.dn( _data.__file__ )
HTML_FG_COLOR = f"rgb{c.Gr.rgb}"
NO_HIGHLIGHT = False

ALL_ATTRIBS = { **globals(),
                **dict([( i, getattr( builtins, i )) for i in filter( lambda x: not x.startswith('_'), dir(builtins) )]),
                **dict([( i, getattr( operator, i )) for i in filter( lambda x: not x.startswith('_'), dir(operator) )])}

def printHelp():
    from texttools import FG as c, Styles as S, Ansi, AnsiList
    opts = [('-a', '--attribute', 'Search for an attribute name'),
            ('-c', '--comments', 'Show comments in output'),
            ('', '', "- default = False"),
            ('-f', '--function', "Function name (or class name) - same as adding ':name' after module name"),
            ('-H', '--html', 'Output an html string'),
            ('-h', '--help', 'Print help message'),
            ('-m', '--module', 'View code from a module, class, or function'),
            ('', '', '- tries as an attribute if all else fails'),
            ('', '', "- will attempt to automagically parse this without the option given"),
            ('-n', '--no-highlighting', 'Disable syntax highlighting in output'),
            ('', '', '- only effects output - string data is still processed'),
            ('', '', "- default = False"),
            ('-p', '--filepath', 'View file contents'),
            ('', '', "- path can also be provided without this option"),
            ('-s', '--string', 'Code view from a provided string'),
            ('', '--version', 'Print version info and exit')]

    R = [ '', f"    {c.gr&S.U}code-view{c._}{c.Gr&S.I} - view highlighted python code{c._}", '' ]
    l_len = max( [ len(i[1]) for i in filter( lambda x: bool( x[1] ), opts ) ])
    od = [ f"{c._&c.dGr&S.B}{i}{c._}" for i in ( '(', '|', ')' ) ]

    for opt in opts:
        if not ( opt[0] or opt[1] ):
            for i in opt[2:]:
                R.append( f"{'':<{l_len+17}}{c.Gr&S.I}{i}{c._}" )
        else:
            s, L, D = AnsiList( opt )
            R.append( f"    {od[0]} {c.Gd&S.I}{s:<2} {od[1]} {c.Gd&S.I}{L:^{l_len}} {od[2]}{c.dl&S.B}: {c._}{c.Gr&S.I} {D}{c._}" )
    R.append('')
    print( '\n'.join(R) )
    return 0

def remove_comments(string):
    quoted = []
    R = []
    s = list(string)
    removed = 0
    last = ''
    while s:
        c = s.pop(0)
        if c in ( '"', "'" ):
            if quoted and quoted[-1] == c:
                quoted.pop(-1)

            else:
                if len(s) >= 2 and all( i == c for i in ( s[0], s[1] )):
                    c += s.pop(0)
                    c += s.pop(0)
                if c in quoted:
                    q_index = quoted.index(c)
                    if q_index == 0:
                        quoted = []
                    else:
                        quoted = quoted[:q_index]

                else:
                    quoted.append(c)

        elif not quoted and c == '#':
            if R and not ''.join(R).split('\n')[-1].strip():
                R = list( '\n'.join( ''.join(R).split('\n')[:-1] ))
                line = len(''.join(R).split('\n'))
                log.debug(f"Removed empty comment line between lines '{line}' and '{line+1}'" )

            removed += 1
            while s and s[0] != '\n':
                s.pop(0)
            continue

        elif c == '\n' and quoted:
            q_index = -1
            if '"""' in quoted:
                _q_index = quoted.index('"""')
                if _q_index > q_index:
                    q_index = _q_index
            elif "'''" in quoted:
                _q_index = quoted.index("'''")
                if _q_index > q_index:
                    q_index = _q_index
            else:
                log.warning(f"Detected invalid quotes in code")

            quoted = [] if q_index < 0 else quoted[:q_index+1]

        R.append(c)

    log.info(f"Removed '{removed}' comments from code lines")
    return ''.join(R)

def highlight_string( string: str, **kwargs ):
    log.debug("Highlighting string")
    log.debug(f"{NO_HIGHLIGHT = }")
    if NO_HIGHLIGHT:
        log.info(f"Skipping highlighting")
        if 'show_comments' in kwargs and not kwargs['show_comments']:
            string = remove_comments(string)
        return Ansi( '\n' + string )
    else:
        SH = SyntaxHighlighter( **kwargs )
        txt = SH.highlight( string )
        return txt

def get_indent(L):
    log.debug(f"Getting indent for line '{L}'")
    n = 0
    if not L.strip():
        return -1
    while L[n] == ' ':
        n += 1
    log.debug(f"Line indent = '{n}'")
    return n

def get_lines(path):
    with open( path, 'r' ) as f:
        lines = f.read().split('\n')
    return lines

def get_code(x):
    code = x.__code__
    lines = get_lines( code.co_filename )
    lineno = code.co_firstlineno - 1
    _indent = get_indent( lines[lineno] )
    end_line = lineno +1
    while not lines[end_line].strip():
        end_line += 1
    indent = get_indent( lines[end_line] )

    while end_line < len(lines) and ( not lines[end_line].strip() or lines[end_line].startswith(f"{'':<{indent}}")):
        end_line += 1
    return '\n'.join([ i[_indent:] for i in lines[ lineno : end_line ] ])

def method_from_file( name, path ):
    log.debug(f"Getting code lines from file '{path}'")
    def _find_index(lines, name):
        for i, line in enumerate(lines):
            if re.match( f"^ *(class|def) {name}\(.*", line ):
                return i
        return -1

    try:
        lines = get_lines(path)
        try:
            start = lines.index( re.search( f"^ *(class|def) {name}\(.*", '\n'.join(lines), re.MULTILINE ).group() )
        except Exception as E:
            log.error(str(E))
            start = _find_index( lines, name )

        if start < 0:
            raise ValueError(f"Couldn't find code data for '{name}' in '{path}'")

        _start_in = get_indent( lines[start] )
        log.debug(f"Starting indent = '{_start_in}'")
        end = start + 1
        while end < len(lines) - 1 and not lines[end].strip():
            end += 1
        _in = get_indent( lines[end] )
        log.debug(f"Method indent level = '{_in}'")

        while start > 0 and lines[ start-1 ].startswith( f"{'':<{_start_in}}@" ):
            start -= 1

        while end < len(lines) - 1 and ( not lines[end+1].strip() or lines[end+1].strip().startswith('#') \
            or lines[end+1].startswith( f"{'':<{_in}}" )):
                end += 1

        return '\n'.join(lines[start:end+1])

    except Exception as E:
        log.exception(E)
        raise

def highlight_module( obj: object, **kwargs ):
    data = ''
    try:
        if not obj:
            raise ValueError(f"Invalid 'obj' argument - '{obj}'")

        if hasattr( obj, '__code__' ):
            data = get_code( obj )

        elif hasattr( obj, '__module__' ):
            mod = imp( obj.__module__ )
            if hasattr( mod, '__code__' ):
                data = get_code( mod )

            elif hasattr( mod, '__file__' ):
                return highlight_file( mod.__file__, **kwargs )
            else:
                raise ValueError(f"No code available for '{obj}'")

        elif hasattr( obj, '__file__' ):
            return highlight_file( obj.__file__, **kwargs )

        else:
            raise ValueError(f"No code available for '{obj}'")

    except Exception as E:
        log.exception(E)
        return ''

    if data:
        return highlight_string( data, **kwargs )
    else:
        return ''

def highlight_function( obj: object, **kwargs ):
    try:
        if not obj:
            raise ValueError(f"Invalid 'obj' argument - '{obj}'")

        data = ''
        if hasattr( obj, '__code__' ):
            return highlight_module( obj, **kwargs )
        elif hasattr( obj, '__module__' ):
            mod = imp( obj.__module__ )
            if hasattr( mod, '__file__' ):
                data = method_from_file( obj.__name__, mod.__file__ )

        if not data:
            raise RuntimeError(f"Can't get function code for '{obj}'")

        return highlight_string( data, **kwargs )

    except Exception as E:
        log.exception(E)
        raise

def highlight_file( path: str, **kwargs ):
    data = ''
    try:
        assert os.path.isfile(path)
        with open( path, 'r' ) as f:
            data = f.read()

    except AssertionError as E:
        log.exception(E)
        log.error(f"Invalid filepath - '{path}'")
    except Exception as E:
        log.exception(E)

    if not data:
        log.error(f"No data found in '{path}'")
        return ''

    return highlight_string( data, **kwargs )

def _view_code_():
    args = sys.argv[1:]
    if not args:
        printHelp()
        print(f"{c.r}  [ERROR]{c.Gr&S.I} no arguments given{c._}\n")
        return 1

    global NO_HIGHLIGHT
    ATTRIB = ''
    DATA = ''
    DATA_TYPE = ''
    COMMENTS = False
    HTML_OUTPUT = False
    txt = ''

    arg = 'None'
    try:
        def chkData():
            if DATA_TYPE:
                raise SyntaxError(f"Data type already specified as '{DATA_TYPE}' - only one data type allowed")

        while args:
            arg = args.pop(0)
            if arg in ( '-a', '--attribute' ):
                if args and not args[0].startswith('-'):
                    ATTRIB = args.pop(0)
                else:
                    ATTRIB = True

            elif arg in ( '-c', '--comments' ):
                COMMENTS = True

            elif arg in ( '-f', '--function' ):
                if not ( DATA_TYPE == 'module' and DATA.find(':') < 0 ):
                    chkData()

                DATA = DATA + ':' + args.pop(0)
                DATA_TYPE = 'module'

            elif arg in ( '-m', '--module' ):
                if not ( DATA_TYPE == 'module' and DATA.startswith(':') ):
                    chkData()

                if DATA:
                    DATA = args.pop(0) + DATA
                else:
                    DATA = args.pop(0)
                    DATA_TYPE = 'module'

            elif arg in ( '-H', '--html' ):
                HTML_OUTPUT = True

            elif arg in ( '-h', '--help' ):
                sys.exit( printHelp() )

            elif arg in ( '-p', '--path' ):
                chkData()
                DATA = args.pop(0)
                DATA_TYPE = 'file'

            elif arg in ( '-s', '--string' ):
                chkData()
                DATA = args.pop(0)
                DATA_TYPE = 'string'

            elif not DATA and Path.isfile(arg):
                DATA = Path.abs( arg )
                DATA_TYPE = 'file'

            elif not DATA and ( arg in locals() or \
                re.match( '^[A-Za-z_]{1}[A-Za-z0-9_]*(\.{1}[A-Za-z_]{1}[A-Za-z0-9_]*)*(:[A-Za-z_]{1}[A-Za-z0-9_]*)?$', arg )):
                    DATA = arg
                    DATA_TYPE = 'module'

            elif arg in ( '-n', '--no-highlighting' ):
                NO_HIGHLIGHT = True

            elif arg == '--version':
                title = Ansi( f"    {c.gr&S.U}code-view{c._}{c.Gr&S.I} - view highlighted python code{c._}" )
                v = Ansi( f"v{c._&c.gr}{__VERSION__}" )
                print( AnsiList( [ '', title, f"{c.S&S.B}{v:^{len(title)}}{c._}", '' ], strsep = '\n' ))
                sys.exit(0)
            else:
                raise SyntaxError(f"Invalid argument '{arg}'")

        if not DATA:
            raise ValueError("Nothing to highlight")

        log.debug(f"{DATA = }, {DATA_TYPE = }")
        if DATA_TYPE == 'module' or ATTRIB:
            log.debug(f"Gathering data from method name '{DATA}'")
            title = []
            module = None
            _func = None
            MOD, FUNC = '', ''
            if DATA.find(':') >= 0:
                MOD, FUNC = DATA.rsplit(':', 1)
                title += [ *MOD.split('.'), FUNC ]
            elif DATA:
                MOD = DATA
                title += MOD.split('.')

            if ATTRIB and isinstance( ATTRIB, str ):
                title.append( ATTRIB )

            log.debug(f"{MOD = }, {FUNC = }")

            if MOD:
                log.debug(f"Searching for '{MOD}' as a module")
                err = ''
                try:
                    try:
                        module = imp( MOD )
                    except Exception as E:
                        err = str(E)
                        try:
                            if MOD.find('.') > 0:
                                module = imp( *MOD.rsplit('.', 1))
                                if module.__name__.split('.')[-1] != MOD.split('.')[-1]:
                                    if FUNC:
                                        try:
                                            m = getattr( module, MOD.split('.')[-1] )
                                            module = m
                                        except:
                                            log.error(f"Couldn't get exact match for '{MOD.split('.')[-1]}'")
                                    else:
                                        FUNC = MOD.split('.')[-1]
                            else:
                                raise
                        except Exception as E:
                            _err = str(E)
                            if _err != err:
                                err += '/n' + _err

                            if not FUNC:
                                log.debug(f"Couldn't find module named '{MOD}' - trying as a global method or attribute")
                                FUNC = MOD
                            else:
                                raise

                except Exception as E:
                    if err:
                        log.error(err)
                    log.error(str(E))

            if FUNC:
                if module:
                    module = getattr( module, FUNC )
                elif FUNC in ALL_ATTRIBS:
                    try:
                        module = ALL_ATTRIBS[FUNC]
                    except:
                        log.error(f"Couldn't find a method named '{FUNC}'")

            if ATTRIB:
                if module:
                    if isinstance( ATTRIB, str ):
                        name = ATTRIB
                        if not hasattr( module, ATTRIB ):
                            raise AttributeError(f"Module '{module}' doesn't contain an attribute named '{ATTRIB}'")
                        attrib = f"{getattr( module, ATTRIB )}"
                    else:
                        name = title[-1]
                        try:
                            if not hasattr( module, '__name__' ) or module.__name__ != title[-1]:
                                m = getattr( module, title[-1] )
                                module = m
                        except:
                            pass

                        attrib = f"{module}"

                elif isinstance( ATTRIB, str ):
                    if not ATTRIB in ALL_ATTRIBS:
                        raise AttributeError(f"Invalid attribute name - '{ATTRIB}'")
                    title = [ 'globals', ATTRIB ]
                    name = ATTRIB
                    attrib = f"{ALL_ATTRIBS[ATTRIB]}"

                else:
                    raise SyntaxError(f"No attribute name provided to search for")

                _func = None
                txt = highlight_string( f"{name} = {attrib}" )

            elif module and hasattr( module, '__file__' ):
                log.info(f"Gathering data for module '{module.__name__}'")
                _func = highlight_module
            elif module and hasattr( module, '__module__' ):
                log.info(f"Gathering data for function '{module.__name__}'")
                _func = highlight_function
            elif module:
                log.info(f"Trying module '{module}' as attribute")
                _func = None
                txt = highlight_string( f"{name} = {module}" )

            else:
                raise AttributeError(f"Couldn't find a method or attribute for '{DATA}'")

            title = f"{c._&c.gr&S.B}.{c._&c.Gr&S.I}".join(title)
            title = Ansi(f"{c._&c.Gr&S.I}{title}{c._}")

            if _func:
                txt = _func( module, show_comments = COMMENTS, remove_leading_whitespace = True )

        elif DATA_TYPE == 'file':
            log.debug(f"Highlighting data from file '{DATA}'")
            title = Ansi(f"{c.ce&S.I}{DATA}{c._}")
            txt = highlight_file( DATA, show_comments = COMMENTS )

        elif DATA_TYPE == 'string':
            log.debug(f"Highlighting provided string '{DATA[:25]}'")
            title = Ansi(f"{c.Gr&S.I}from string{c._}")
            txt = highlight_string( DATA, show_comments = COMMENTS, remove_leading_whitespace = True )

    except Exception as E:
        log.exception(E)
        sys.exit(1)

    # Adding title to output
    if txt and HTML_OUTPUT:
        if NO_HIGHLIGHT:
            html_title = f"Python Code View - {title.clean}"
        else:
            html_title = Ansi( f"{c.S&S.U}Python Code View{c._&c.Gr&S.I} - {c.ce}{title}{c._}" ).html()

        with open( HTML_TEMPLATE, 'r' ) as f:
            template = f.read()

        html_txt = txt.html()
        bg_color = f"rgb{CODE_BACKGROUND.rgb}"
        html = template.replace( '__SRC__', DATA_DIR ).replace( '__CODEVIEW_TITLE__', html_title )
        html = html.replace( '__BG_COLOR__', bg_color ).replace( '__FG_COLOR__', HTML_FG_COLOR )
        html = html.replace( '__CODEVIEW__', html_txt )
        print( html )
        sys.exit(0)

    elif txt:
        txt = str(AnsiList( [ '', f"  {c.S&S.U}Python Code View{c._&c.Gr&S.I} - {c.ce}{title}{c._}",
                              *[ f"    {i}" for i in str(txt).split('\n') ], "" ],
                            strsep = '\n' ))

        if NO_HIGHLIGHT:
            print( txt.clean )
        else:
            print(txt)
        sys.exit(0)

    else:
        print(f"\n{c.r}  [ERROR]{c.Gr&S.I} nothing to print{c._}\n")
        sys.exit(1)

if __name__ == "__main__":
    _view_code_()
