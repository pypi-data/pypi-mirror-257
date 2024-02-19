import re, colorsys
from importlib import import_module
from ._constants import ANSI_MOD_PERCENTAGE
from apputils import listFlatten

def _setXtra_(cls):
    setattr( cls, 'dim'         , lambda n = 10: _dim_(cls, n)    )
    setattr( cls, 'bright'      , lambda n = 10: _bright_(cls, n) )
    setattr( cls, 'blend'       , lambda obj, n = 5: _blend_(cls, obj, n)  )
    setattr( cls, 'invert'      , lambda: _invert_(cls) )
    setattr( cls, 'hsv'         , lambda: _hsv_(cls) )
    setattr( cls, 'hsv_to_rgb'  , classmethod( lambda _cls, hsv: hsv_to_rgb( hsv )))

def hsv_to_rgb( hsv ):
    h, s, v = hsv
    if h > 1:
        h = h / 359
    if s > 1:
        s = s / 255
    return tuple( int(round(i)) for i in colorsys.hsv_to_rgb( h, s, v ))

def __percent__(n = 0):
    import logging
    log = logging.getLogger(__name__)
    try:
        if isinstance( n, str ):
            assert re.match( '^[0-9]*\.?[0-9]+$', n )
            if n.find('.') >= 0:
                n = float(n)
            else:
                n = int(n)

        n = abs(n)
        if ( isinstance( n, int ) and n >= 1 ) or n > 1:
            return n*.01
        return n
    except Exception as E:
        log.exception(E)
        raise

def _hsv_(cls):
    hsv = list( colorsys.rgb_to_hsv( *cls.rgb ))
    hsv[0] = int(round( 359 * hsv[0] ))
    hsv[1] = int(round( 255 * hsv[1] ))
    return tuple(hsv)

def _get_color_types(item, *, _FG = None, _BG = None):
    if _FG and _BG:
        return _FG, _BG
    elif isinstance( item, AnsiCombo ):
         for i in item.extended():
            _FG, _BG = getAttribs(i)
    elif not _FG and isinstance( item, FG_Color ):
        _FG = item
        return _FG, _BG
    elif not _BG and isinstance( item, BG_Color ):
        _BG = item
        return _FG, _BG


def _bg_(cls):
    from . import newColor
    from .types import FG_Color, BG_Color, AnsiCombo
    _FG, _BG = None, None
    _FG, _BG = _get_color_types( cls )
    if _BG:
        return _BG
    return newColor( _FG.rgb )

def _fg_(cls):
    from . import getColor
    from .types import FG_Color, BG_Color, AnsiCombo
    _FG, _BG = None, None
    _FG, _BG = _get_color_types( cls )
    if _FG:
        return _FG
    return Colors.fromRGB( _BG.rgb )

def _bright_(cls, n = ANSI_MOD_PERCENTAGE):
    from .color_mods import Brightened, _mod_val
    p = __percent__(n)

    if hasattr( cls, 'blend_val' ):
        A, B = ( _bright_( i, n ) for i in cls.bases )
        return A.blend( B, cls.blend_val )
    elif any( hasattr( cls, i ) for i in ['bright_value', 'dim_value'] ):
        obj = cls.base
        print(f"{obj = }")
        new_rgb = Brightened._bright_( cls.rgb, p )
        print(f"{new_rgb = }")
        mod, val = _mod_val( cls.base, new_rgb )
        print(f"{mod = }, {val = }")
        if mod == 'base':
            return obj
        return getattr( obj, mod )( val )
    else:
        obj = cls
        val = p

    return Brightened( obj, p )

def _dim_(cls, n = ANSI_MOD_PERCENTAGE):
    from .color_mods import Dimmed, _mod_val
    p = __percent__(n)

    if hasattr( cls, 'blend_val' ):
        A, B = ( _dim_( i, n ) for i in cls.bases )
        return A.blend( B, cls.blend_val )
    elif any( hasattr( cls, i ) for i in ['bright_value', 'dim_value'] ):
        obj = cls.base
        print(f"{obj = }")
        new_rgb = Dimmed._dim_( cls.rgb, p )
        print(f"{new_rgb = }")
        mod, val = _mod_val( cls.base, new_rgb )
        print(f"{mod = }, {val = }")
        if mod == 'base':
            return obj
        return getattr( obj, mod )( val )
    else:
        obj = cls
        val = p

    return Dimmed( cls, p )

def _blend_(cls, other, n = ANSI_MOD_PERCENTAGE):
    from .color_mods import Blended
    p = __percent__(n)
    return Blended( cls, other, p )

def _invert_(cls):
    if hasattr( cls, 'revert' ):
        return cls.revert()
    from .color_mods import Inverted
    return Inverted(cls)

def getColors( itemA, itemB = None ):
    from .types import FG_Color, BG_Color, Style
    if itemB == None:
        if not itemA.extended():
            return { type(itemA): itemA }
        return dict( [[( type(i), i ) for i in filter( lambda x: isinstance( x, FG_Color|BG_Color ), itemA.extended() )][0]] )

    colorsA  = dict([( type(i), i ) for i in filter( lambda x: isinstance( x, FG_Color|BG_Color ), itemA.extended() )])
    if not colorsA:
        colorsA = { type(itemA): itemA }

    colorsB = dict([( type(i), i ) for i in filter( lambda x: isinstance( x, FG_Color|BG_Color ), itemB.extended() )])
    if not colorsB:
        colorsB = { type(itemB): itemB }

    return ( colorsA, colorsB )

def cleanRep(rep, *obj_names):
    import logging
    log = logging.getLogger(__name__)

    def rmName(s, m):
        i = s.find(m)
        m_end = i+len(m)+1
        cnt = s[:m_end].count('(')
        tot = s[m_end:].count(')') - cnt
        n = len(s)
        while s[m_end:n].count(' )') > tot:
            n -= 1

        mid = s[m_end-1:n]
        rmP = re.search( ' - \[%[0-9]+\] ?$', mid )
        if rmP:
            mid = mid[:-len(rmP.group())]

        R = ( s[:i] + mid + s[n+1:] ).strip()
        return R

    _C = 2
    log.debug(f"Cleaning __repr__ for '{rep}'")
    log.debug(f"  1 - {rep}")
    rep = rep.replace('>','').replace('<','')
    log.debug(f"  2 - {rep}")

    for nm in re.findall( 'Ansi[A-Za-z]{5}\(', rep ):
        rep = rmName( rep, nm )

    for nm in ( 'Ansi[A-Za-z]{5}', *obj_names ):
        rm = "{nm}\("
        for i in re.findall( rm, rep ):
            rep = rmName( rep, i )
            _C += 1
            log.debug(f"  {_C} - {rep}")

    R = []
    _CHn = 65
    for name in rep.split('+'):
        _CH = 97
        log.debug(f"    {_C}.{chr(_CHn)}.{chr(_CH)} - '{name}'")
        _CH += 1
        log.debug(f"    {_C}.{chr(_CHn)}.{chr(_CH)} - '{name}'")
        _CH += 1
        name = name.strip()
        if not name.strip():
            log.debug(f"    {_C}.{chr(_CHn)}.{chr(_CH)} - Skipping empty name")
            continue

        if re.match( '^[A-Za-z]\(', name ):
            if not name.endswith(')'):
                name += ' )'
                log.debug(f"    {_C}.{chr(_CHn)}.{chr(_CH)} - '{name}'")
                _CH += 1

        while name.count(')') > name.count('('):
            name = re.sub( ' ?)', '', name, 1 ).strip()
            log.debug(f"    {_C}.{chr(_CHn)}.{chr(_CH)} - '{name}'")
            _CH += 1

        R.append(name)
        _CHn += 1

    rep = ' + '.join(R)
    log.debug(f"    {_C} - {rep = }")
    return rep

# AnsiCombo Methods

class ComboFuncs:
    def bg(self): return list(filter( lambda x: isinstance( x, BG_Color ),
                                      self.extended() ))[0] if self.hasBG() else None
    def fg(self): return list(filter( lambda x: isinstance( x, FG_Color ),
                                      self.extended() ))[0] if self.hasFG() else None
    def hasBG(self): return self.hasEscape( 'bg_color' )
    def hasFG(self): return self.hasEscape( 'fg_color' )
    def hasBlink(self): return self.hasEscape( 'blink' )
    def hasBold(self): return self.hasEscape( 'bold' )
    def hasEscape(self, escape): return escape.lower() in [ type(i).__name__.lower() for i in self.__ext__.values() ]
    def hasItalic(self): return self.hasEscape( 'italic' )
    def hasStrikethrough(self): return self.hasEscape( 'strikethrough' )
    def hasUnderline(self): return self.hasEscape( 'underline' )
    def hasReset(self): return self.hasEscape( 'reset' )

# AnsiEscape Methods

class EscapeFuncs:
    def escapes(cls):
        """ Return flattened list of escape integers """
        return listFlatten( cls.__esc__, tuples = True )

    def extended(cls):
        """ Return list of extended escape values """
        return [ v for v in cls.__ext__.values() ]

    def extendedItems(cls):
        """ Return item list of extended escapes """
        return [ ( k, v ) for k, v in cls.__ext__.items() ]

    def extendedNames(cls):
        """ Return list of extended escape names """
        return [ key for key in cls.__ext__.keys() ]

    def extendedTypes(cls):
        """ Return list of extended types """
        return [ type(ext) for ext in cls.__ext__.values() ]

    def hex_codes(cls):
        def getHex(_h):
            return '#'+''.join([ f"%0{int(6/len(_h))}x" for i in range(int(len(_h))) ])%_h

        st_type = { 0: 'reset', 1: 'bold', 3: 'italic', 4: 'underline', 5: 'blink', 9: 'strikethrough' }
        fg, bg, styles = '', '', {}
        for esc in cls.extended():
            s = ','.join(esc)
            if s.startswith('38,2'):
                h['fg'] = getHex(esc)
            elif s.startswith('48,2'):
                h['bg'] = getHex(esc)
            else:
                styles[st_type[esc[0]]] = getHex(esc)

        H = { 'fg': fg,
              'bg': bg,
              'styles': None if not styles else type( 'styles', (), styles )() }

        return type( 'HexCodes', (), H )()

    def htmlItems(cls):
        return [ (k, v) for k, v in cls.__html__.items() ]

    def htmlStyle(cls):
        return f'''style="{'; '.join([ f'{k}: {v}' for k, v in cls.__html__.items() ])};"'''

    def htmlKeys(cls):
        return [ k for k in cls.__html__.keys() ]

    def htmlValues(cls):
        return [ v for v in cls.__html__.values() ]

    def objects(cls):
        R = cls.extended()
        return R if R else [cls]

    def prefix(cls):
        """ Return color prefix tuple """
        return cls.__pre__

# _EscapeFuncs = { 'escapes'      : escapes,
#                  'extended'     : extended,
#                  'extendedItems': extendedItems,
#                  'extendedNames': extendedNames,
#                  'extendedTypes': extendedTypes,
#                  'hex_codes'    : hex_codes,
#                  'htmlItems'    : htmlItems,
#                  'htmlStyle'    : htmlStyle,
#                  'htmlKeys'     : htmlKeys,
#                  'htmlValues'   : htmlValues,
#                  'prefix'       : prefix        }
