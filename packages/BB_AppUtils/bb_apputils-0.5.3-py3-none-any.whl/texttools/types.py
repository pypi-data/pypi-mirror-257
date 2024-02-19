import os, re   #, logging
from logging import getLogger
from functools import wraps, update_wrapper
from glob import glob
from datetime import datetime as dt
from typing import Union

from ._constants import ( COMPARE_FUNCTIONS,
                          STRING_FUNCTIONS,
                          RE_RGB_ESCAPE,
                          RE_16COLOR_ESCAPE,
                          RE_STYLE_ESCAPE,
                          ANSI_MOD_PERCENTAGE )
from .ansitools import Ansi
from apputils import listFlatten, isSafeAttribName, AppData, Path
from . import _type_functions as _tf
from ._type_functions import ( __percent__,
                               _setXtra_,
                               _bright_,
                               _dim_,
                               _blend_,
                               _invert_,
                               ComboFuncs,
                               EscapeFuncs,
                               cleanRep )

class AnsiEscapeMeta(type):
    def __new__(cls, name, bases, clsDict):
        clsDict = { '__com__'          : '',
                    '__dir__'          : cls.__dir__,
                    '__doc__'          : '',
                    '__esc__'          : (),
                    '__ext__'          : {},
                    '__instancecheck__': cls.__instancecheck__,
                    '__invert__'       : cls._mod_wrapper_( cls.__invert__ ),        # TODO
                    '__pre__'          : '',
                    '__html__'         : {},
                    '__neg__'          : cls._mod_wrapper_( cls.__neg__ ),
                    '__pos__'          : cls._mod_wrapper_( cls.__pos__ ),
                    '__or__'           : cls._ior_wrapper_( cls.__ior__ ),
                    '__rep__'          : '',
                    '__s__'            : Ansi(),
                    '_code_'           : '',
                    'name'             : '',
                    'rgb'              : (),
                    'ansi'             : (),
                    **clsDict   }

        clsDict['__ior__'] = clsDict['__or__']
        R = type.__new__( cls, name, bases + (EscapeFuncs,), clsDict )
        super( EscapeFuncs, R ).__init__(R)
        return R

    def __dir__(self):
        R = set()
        for cls in self.mro() + [EscapeFuncs]:
            R |= set( list( cls.__dict__.keys() ))
        return sorted(R)

    def __instancecheck__(self, other):
        if hasattr( other, '__bases__' ) and self in other.__bases__:
            return True

        types = [ type(other) ]
        if hasattr( other, '__ext__' ) and len(other.__ext__) >= 2:
            types += [ *other.extendedTypes(), AnsiCombo ]

        types = set(types)
        if self in types:
            return True
        else:
            return super().__instancecheck__(other)

    def _ior_wrapper_(func):
        @wraps(func)
        def __inner(self, other, n = ANSI_MOD_PERCENTAGE):
            try:
                if func.__name__ == '__ror__':
                    assert isinstance( other, AnsiEscape ) and hasattr( other, '__or__' )
                    return func( self, other, n )

                types = set( [type(self)]+[ type(i) for i in filter( lambda x: isinstance( x, FG_Color|BG_Color ), [ v for k, v in self.__ext__.items() ])])
                othertypes = set( [type(other)]+[ type(i) for i in filter( lambda x: isinstance( x, FG_Color|BG_Color ), [ v for k, v in other.__ext__.items() ])])
                n = __percent__(n)
                if not types:
                    raise RuntimeError
                assert othertypes
                if not types & othertypes:
                    raise ValueError
            except RuntimeError:
                raise TypeError(f"{repr(self)} doesn't support the blend method")
            except AssertionError:
                raise TypeError(f"{repr(other)} doesn't support the blend method")
            except ValueError:
                raise ValueError(f"No shared color types to blend {repr(self)} and {repr(other)}")

            return func( self, other, n )
        return __inner

    def _mod_wrapper_(func):
        @wraps(func)
        def __inner(cls, n = ANSI_MOD_PERCENTAGE):
            attr = { '__neg__': 'dim', '__pos__': 'bright', '__invert__': 'invert' }
            if not hasattr( cls, attr[ func.__name__ ] ):
                raise TypeError(f"Ansi type '{type(self).__name__}' has no attribute '{attr[func.__name__]}'")
            return func(cls, n)
        return __inner

    def __neg__(self, n):
        return _dim_( self, n )
    def __pos__(self, n):
        return _bright_( self, n )
    def __invert__(self, n):
        return _invert_( self )
    def __ior__(self, other, n):
        return _blend_( self, other, n )

class AnsiEscape(metaclass = AnsiEscapeMeta):
    def _Escape_Wrapper_(func):
        """ Wrapper for FG_Color, BG_Color and Style types """
        @wraps(func)
        def __inner(self, other = 'pass'):
            # log = getLogger(__name__)
            fn = func.__name__
            try:
                if other == 'pass':
                    return

                assert isinstance( other, AnsiEscape )
                # log.debug(f"{self = }, {other = }, {func = }")
                if fn in ( '__eq__', '__ne__' ):
                    _self, _other = self.escapes(), other.escapes()
                elif self.name == other.name:
                    _self, _other = len( self.escapes() ), len( other.escapes() )
                elif self.name.split()[-1] != other.name.split()[-1]:
                    _self, _other = self.name.split()[-1], other.name.split()[-1]
                else:
                    _self, _other = self.name, other.name

                # log.debug(f"{_self = }, {_other = }")
                return func( self, _self, _other )

            except:
                pass
        return __inner

    def __format__( self, format_spec = '' ): return Ansi( f"\x1b[{';'.join([ str(i) for i in listFlatten( self.__esc__, tuples = True ) ])}m" ).__format__( format_spec )
    def __str__(self)                       : return Ansi( f"\x1b[{';'.join([ str(i) for i in listFlatten( self.__esc__, tuples = True ) ])}m" )
    def __len__(self)                       : return len( Ansi( '\x1b[' + ';'.join([ str(i) for i in listFlatten( self.__esc__, tuples = True ) ]) + 'm' ) )
    def __bool__(self)                      : return True
    def __add__( self, other )              : return Ansi( f"\x1b[{';'.join([ str(i) for i in listFlatten( self.__esc__, tuples = True ) ])}m{other}" )
    def __radd__( self, other )             : return Ansi( f"{other}\x1b[{';'.join([ str(i) for i in listFlatten( self.__esc__, tuples = True ) ])}m" )
    # def __repr__(self)                      : return self.__rep__
    @_Escape_Wrapper_
    def __eq__( self, _self, other ): return _self == other
    @_Escape_Wrapper_
    def __ne__( self, _self, other ): return _self != other
    @_Escape_Wrapper_
    def __gt__( self, _self, other ): return _self >  other
    @_Escape_Wrapper_
    def __ge__( self, _self, other ): return _self >= other
    @_Escape_Wrapper_
    def __lt__( self, _self, other ): return _self <  other
    @_Escape_Wrapper_
    def __le__( self, _self, other ): return _self <= other

    def _and_wrapper_(func):
        @wraps(func)
        def __inner(self, other, **kwargs):
            # log = logging.getLogger(__name__)
            if not isinstance( other, AnsiEscape ):
                # log.debug(f"Not an AnsiEscape object 'other' = '{type(other)}'")
                if isinstance( other, str|Ansi ):
                    if func.__name__ == '__and__':
                        # log.debug("Returning as a string using __add__")
                        return self.__add__( other )
                    else:
                        # log.debug("Returning as a string using __radd__")
                        return self.__radd__( other )
                raise TypeError(f"Can only add attributes from other AnsiEscape types, not '{type(other)}'")

            _reset = None
            try:
                objects = []
                if self.__ext__:
                    self_types = self.extendedTypes()
                    objects += list( self.__ext__.values() )
                else:
                    self_types = [ type(self) ]
                    objects.append( self )

                if other.__ext__:
                    others_types = other.extendedTypes()
                    other_ext = list( other.__ext__.values() )
                    if isinstance( other_ext[0], Reset ):
                        _reset = other_ext.pop(0)
                        if not isinstance( objects[0], Reset ):
                            objects.insert( 0, _reset )
                    objects += other_ext

                else:
                    if isinstance( other, Reset ):
                        raise TypeError("Can't add 'Reset' type to another attribute")
                    others_types = [ type(other) ]
                    objects.append( other )

                type_list = [ type(i) for i in objects ]
                if any( type_list.count( i ) > 1 for i in ( FG_Color, BG_Color )):
                    raise ValueError(f"'{self.__name__}' already contains attribute type '{type(other).__name__}'")

                names = [ i.__name__.replace('rm_','') for i in objects ]
                if len(set(names)) < len(names):
                    matches = list(filter( lambda x: names.count(x) > 1, names ))
                    raise ValueError(f"Attributes already found in '{self.__name__}' - '{matches}'")

                R = objects.pop(0)
                # log.debug(f"{R = }")
                while objects:
                    R = Combo( R, objects.pop(0), **kwargs )
                    # log.debug(f"{R = }")
                return R

            except Exception as E:
                # log.exception(E)
                raise
        return __inner

    @_and_wrapper_
    def __rand__(self, other):
        return str(other)+str(self)
    @_and_wrapper_
    def __and__(self, other):
        return str(self)+str(other)
    def __hash__(self):
        return sum( self.escapes() )

class FG_Color(type, AnsiEscape):
    def __repr__(self): return self.__rep__
    def bg(self): return AnsiColor( name = self.__name__,
                                    code = self._code_,
                                    prefix = (48,2),
                                    rgb = self.rgb,
                                    comment = self.__com__  )
    def fg(self): return self

class BG_Color(type, AnsiEscape):
    def __repr__(self): return self.__rep__
    def fg(self): return AnsiColor( name = self.__name__[3:],
                                    code = self._code_,
                                    prefix = (38,2),
                                    rgb = self.rgb,
                                    comment = self.__com__  )
    def bg(self): return self

class Style(type, AnsiEscape):
    def __repr__(self): return self.__rep__

class Blink(Style):
    pass
class Bold(Style):
    pass
class Italic(Style):
    pass
class Strikethrough(Style):
    pass
class Underline(Style):
    pass

class Reset(type, AnsiEscape):
    def __repr__(self): return self.__rep__

class AnsiCombo(type, AnsiEscape):
    def __repr__(self): return self.__rep__

class AnsiColor:
    """ Color Escape """

    def __new__( cls, *args, name, code, prefix, rgb, ext = {}, comment = '', **kwargs ):
        rgb = tuple(rgb)
        pre = tuple(prefix)
        esc = pre + rgb
        html = {}

        if pre == (38,2):
            _name = name.title().replace('_',' ').strip()
            base_type = FG_Color
            doc = f"Ansi foreground color"
            html = { 'color': f"rgb{rgb}" }
        elif pre == (48,2):
            _name = name.title().replace('_',' ').strip()
            base_type = BG_Color
            doc = f"Ansi background color"
            html = { 'background-color': f"rgb{rgb}" }
        else:
            raise TypeError(f"Invalid prefix for AnsiColor '{pre}'")

        if '_name' in kwargs:
            _name = kwargs['_name']

        rep = f"AnsiColor(< {_name} >)"

        if comment:
            doc += f"\n  - {comment}"

        clsDict = { '_code_'   : code,
                    '__com__'  : comment,
                    '__doc__'  : doc,
                    '__esc__'  : esc,
                    '__ext__'  : ext,
                    '__html__' : html,
                    '__pre__'  : pre,
                    '__rep__'  : rep,
                    'hex'      : '#%02x%02x%02x'%rgb,
                    'name'     : _name,
                    'rgb'      : rgb,
                    }

        R = type.__new__( base_type, name, (), clsDict )
        _setXtra_(R)
        return R

class AnsiStyle:
    """ Style escape """

    def __new__( cls, *args, name, code, html, ansi, key = '', ext = {}, comment = '' ):
        ansi = tuple(ansi)
        _name = name.title().replace('_',' ').strip()

        rep = f"AnsiStyle(< {_name} >)"
        if comment:
            doc = f"Ansi style: {_name}\n  - {comment}"
        else:
            doc = f"Ansi style: {_name}"

        if name == 'reset':
            base_type = Reset
        else:
            base_type = globals()[ name.split('_')[-1].title() ]

        esc = ansi
        ext = {}
        pre = ()

        clsDict = { '_code_'  : code,
                    '__com__' : comment,
                    '__doc__' : doc,
                    '__esc__' : esc,
                    '__ext__' : ext,
                    '__html__': html,
                    '__pre__' : pre,
                    '__rep__' : rep,
                    'name'    : _name,
                    'ansi'    : ansi,
                    }

        return type.__new__( base_type, name, (), clsDict )

class Combo:
    """ Ansi esccape combination """

    def __new__( cls, base, other, *, key = '', **kwargs ):
        baserep = cleanRep( base.__rep__ )
        otherrep = cleanRep( other.__rep__ )

        doc   = f"AnsiCombo: {baserep.replace('+','&')} & {otherrep}"
        code  = base._code_ + '_' + other._code_
        if not base.__ext__:
            bext = { base.__name__: base }
        else:
            bext = base.__ext__

        ext   = { **bext, other.__name__: other }
        esc   = tuple( v.__esc__ for k, v in ext.items() )
        if key:
            rep   = f"AnsiCombo(< {baserep} + {otherrep} [{key}] >)"
            name  = f"{baserep} + {otherrep} ({key})"
            doc = f"{doc} ({key})"
            clsName = f"{key}.AnsiCombo"
        else:
            clsName = "AnsiCombo"
            name  = f"{baserep} + {otherrep}"
            rep   = f"AnsiCombo(< {baserep} + {otherrep} >)"

        styles = ('blink','bold','italic','underline','reset','strikethrough')
        _has = dict([( '__'+i+'__', False ) for i in styles ])
        rgb = { 'rgb': (), 'bg_rgb': () }
        objects = {}
        for k, v in ext.items():
            if v.__com__:
                doc += f"\n    - {v.__com__}"

            if isinstance( v, FG_Color ):
                rgb['rgb'] = v.rgb
            elif isinstance( v, BG_Color ):
                rgb['bg_rgb'] = v.rgb
            elif k in styles:
                _has[ '__' + k + '__' ] = True

            objects[k] = v

        html = base.__html__.copy()
        for k, v in other.__html__.items():
            if k in html and html[k] not in ( 'normal', 'none' ):
                html[k] = f"{html[k]} {v}"
            else:
                html[k] = v

        bases = (ComboFuncs,)
        if '__type__' in kwargs:
            bases = bases + (kwargs.pop('__types__'),)

        clsDict = { '_code_': code,
                    '__rep__' : rep,
                    '__esc__' : esc,
                    '__doc__' : doc,
                    '__ext__' : ext,
                    '__pre__' : (),
                    '__html__': html,
                    'name'    : name,
                    **kwargs,
                    **rgb,
                    **_has,
                    }

        R = type.__new__( AnsiCombo, clsName, bases, clsDict )
        super( ComboFuncs, R ).__new__(R)
        for n, item in R.__ext__.items():
            setattr( R, n, item )

        if any( i in [ type(a) for a in R.extended() ] for i in ( FG_Color, BG_Color )):
            _setXtra_(R)
        return R
