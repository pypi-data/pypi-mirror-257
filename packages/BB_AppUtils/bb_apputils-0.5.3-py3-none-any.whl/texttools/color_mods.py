from typing import Union

from apputils import listFlatten
from .types import FG_Color, BG_Color, AnsiEscape, AnsiCombo, Style
from .ansitools import Ansi, AnsiList
from logging import getLogger
from ._type_functions import cleanRep, getColors, _setXtra_

def _mod_val( orig, rgb ):
    from apputils import tupleCalc as tc
    print(f"{orig.rgb = }, {rgb = }")
    # print(f"{tc( orig.rgb, rgb, '/' ) = }")
    # print(f"{tc( rgb, orig.rgb, '/' ) = }")

    if orig.rgb == rgb:
        return ( 'base', 0 )
    elif all( a >= b for a, b in zip( orig.rgb, rgb )):
        values = tuple( i for i in filter( lambda x: x != 0, tc( rgb, orig.rgb, '/' )))
        return ( 'dim', 1 - sum([ i/len(values) for i in values ]))
    elif all( a <= b for a, b in zip( orig.rgb, rgb )):
        diff = tc( 255, orig.rgb, '-' )
        rgb_diff = tc( rgb, orig.rgb, '-' )
        values = tuple( i for i in filter( lambda x: x != 0, tc( orig.rgb, rgb, '/' )))
        return ( 'bright', sum([ i/len(values) for i in values ]))
    else:
        raise ValueError("Invalid rgb values")

class Dimmed(type):
    def __new__( cls, obj, n ):
        if n < 0 or n > 1:
            raise ValueError(f"'n' must be a value between 0 and 1")

        dim_val = n
        ext = {}

        colors = getColors(obj)
        # b_name = cleanRep( ' + '.join([ i.__rep__ for i in colors.values() ]), 'Dimmed' ) +  f" - [%{int(n*100)}]"

        name = f"{obj.__name__}_dimmed"
        code = '_'.join([ i._code_ for i in colors ]) + '_dimmed'

    # Combo
        if isinstance( obj, AnsiCombo ):
            s_names = []
            c_names = []
            html = {}
            doc = ''
            # rgb_values = {}
            for k, v in obj.__ext__.items():
                if not isinstance( v, FG_Color|BG_Color ):
                    nm, item = k, v
                    ext[nm] = item
                    s_names.append( cleanRep( item.__rep__ ))
                else:
                    item = v.dim(n)
                    c_names.append( cleanRep( item.base.__rep__, 'Dimmed', 'Brightened' ))
                    nm = item.__name__
                    ext[nm] = item
                    # rgb_values[ 'rgb' if isinstance( item, FG_Color ) else 'bg_rgb' ] = item.rgb

                if item.__com__:
                    doc += f"\n    - {item.__com__}"
                html = { **html, **item.__html__ }
                del nm, item

            # if 'rgb' not in rgb_values:
                # rgb_values['rgb'] = rgb_values.pop('bg_rgb')

            c_names = ' + '.join( sorted( c_names ))
            if s_names:
                s_names = ' + ' + ' + '.join( sorted( s_names ))
            else:
                s_names = ''

            rep   = f"AnsiCombo(< Dimmed( {c_names} - [%{int(n*100)}] ) + {' + '.join(s_names)} >)"
            _name = f"AnsiCombo: {c_names}{s_names} (Dimmed)"
            doc   = _name.replace('+','&')
            esc   = tuple( v.__esc__ for v in ext.values() )

            R = type.__new__( AnsiCombo, name, (), { '_code_'   : code,
                                                     '__doc__'  : doc,
                                                     '__esc__'  : esc,
                                                     '__ext__'  : ext,
                                                     '__pre__'  : (),
                                                     '__rep__'  : rep,
                                                     '__html__' : html,
                                                     'dim_value': dim_val,
                                                     'name'     : _name     })
            _setXtra_(R)
            return R

    # Color
        elif isinstance( obj, FG_Color ):
            base_type = FG_Color
        elif isinstance( obj, BG_Color ):
            base_type = BG_Color
        else:
            raise TypeError(f"Not a dimmable type - {type(obj)}")

        b_name = cleanRep( ' + '.join([ i.__rep__ for i in colors.values() ]), 'Dimmed' ) +  f" - [%{int(n*100)}]"

        _name = f"{b_name} (Dimmed)"
        rep = f"Dimmed(< {b_name} >)"
        doc = _name.replace('+','&')
        rgb = cls._dim_( obj.rgb, dim_val )
        esc = obj.__pre__ + rgb

        if base_type == FG_Color:
            html = { 'color': f"rgb{rgb}" }
        else:
            html = { 'background-color': f"rgb{rgb}" }

        R = type.__new__( base_type, name, (), {
                                                 '__com__'   : obj.__com__,
                                                 '__doc__'   : doc,
                                                 '__esc__'   : esc,
                                                 '__ext__'   : ext,
                                                 '__html__'  : html,
                                                 '__pre__'   : obj.__pre__,
                                                 '__rep__'   : rep,
                                                 '_code_'    : code,
                                                 'base'      : obj,
                                                 'dim_value' : dim_val,
                                                 'name'      : _name,
                                                 'rgb'       : rgb     })
        _setXtra_(R)
        return R

    @classmethod
    def _dim_(cls, rgb, n):
        from apputils import tupleCalc as tc
        RGB = []
        diff = tc( rgb, n, '*', round_int = True )
        for i in range(len(rgb)):
            a = 0 if diff[i] > rgb[i] else rgb[i] - diff[i]
            RGB.append(a)
            del a

        return tuple(RGB)

class Brightened(type):
    def __new__( cls, obj, n ):
        if n < 0 or n > 1:
            raise ValueError(f"'n' must be a value between 0 and 1")

        br_val = n
        ext = {}

        colors = getColors( obj )
        # b_name = cleanRep( ' + '.join([ i.__rep__ for i in colors.values() ]), 'Brightened' ) +  f" - [%{int(n*100)}]"

        name = f"{obj.__name__}_brightened"
        code = '_'.join([ i._code_ for i in colors ]) + '_brightened'

            # rep = f"Brightened(< {_name} -[ %{int(n*100)} ] >)"
            # _name = f"{_name} (Brightened)"
    # Combo
        if isinstance( obj, AnsiCombo ):
            # rgb_values = {}
            html = {}
            s_names = []
            c_names = []
            doc = ''
            for k, v in obj.__ext__.items():
                if not isinstance( v, FG_Color|BG_Color ):
                    nm, item = k, v
                    ext[nm] = item
                    s_names.append( cleanRep( item.__rep__ ))
                else:
                    item = v.bright(n)
                    c_names.append( cleanRep( item.base.__rep__, 'Dimmed', 'Brightened' ))
                    nm = item.__name__
                    ext[nm] = item
                    # rgb_values[ 'rgb' if isinstance( item, FG_Color ) else 'bg_rgb' ] = item.rgb

                if item.__com__:
                    doc += f"\n    - {item.__com__}"
                html = { **html, **item.__html__ }
                del nm, item

            # if 'rgb' not in rgb_values:
                # rgb_values['rgb'] = rgb_values.pop('bg_rgb')

            c_names = ' + '.join(c_names)
            if s_names:
                s_names = ' + ' + ' + '.join(s_names)
            else:
                s_names = ''

            rep   = f"AnsiCombo(< Brightened( {c_names} - [%{int(n*100)}] ){s_names} >)"
            _name = f"AnsiCombo: {c_names}{s_names} (Brightened)"
            doc   = f"{_name.replace('+','&')}{doc}"

            esc = tuple( v.__esc__ for v in ext.values() )
            R = type.__new__( AnsiCombo, name, (), { '_code_'      : code,
                                                     '__doc__'     : doc,
                                                     '__esc__'     : esc,
                                                     '__ext__'     : ext,
                                                     '__pre__'     : (),
                                                     '__rep__'     : rep,
                                                     '__html__'    : html,
                                                     'bright_value': br_val,
                                                     'name'        : _name      })
            _setXtra_(R)
            return R

    # Color
        elif isinstance( obj, FG_Color ):
            base_type = FG_Color
        elif isinstance( obj, BG_Color ):
            base_type = BG_Color
        else:
            raise TypeError(f"Type {type(obj)} can not be brightened")

        b_name = cleanRep( ' + '.join([ i.__rep__ for i in colors.values() ]), 'Brightened' ) +  f" - [%{int(n*100)}]"

        rep   = f"Brightened(< {b_name} >)"
        _name = f"{b_name} (Brightened)"
        doc = f"Brightened: {obj.__doc__}"
        rgb = cls._bright_( obj.rgb, br_val )
        esc = obj.__pre__ + rgb

        if base_type == FG_Color:
            html = { 'color': f"rgb{rgb}" }
        else:
            html = { 'background-color': f"rgb{rgb}" }

        R = type.__new__( base_type, name, (), { '_code_'      : code,
                                                 '__com__'     : obj.__com__,
                                                 '__doc__'     : doc,
                                                 '__esc__'     : esc,
                                                 '__ext__'     : ext,
                                                 '__html__'    : html,
                                                 '__pre__'     : obj.__pre__,
                                                 '__rep__'     : rep,
                                                 'base'        : obj,
                                                 'bright_value': br_val,
                                                 'name'        : _name,
                                                 'rgb'         : rgb     })
        _setXtra_(R)
        return R

    @classmethod
    def _bright_(cls, rgb, n):
        from apputils import tupleCalc as tc
        RGB = []
        _diff = [ 255 - i for i in rgb ]
        diff = tc( _diff, n, '*', round_int = True )
        for i in range(len(rgb)):
            a = diff[i] + rgb[i]
            if a > 255:
                a = 255
            RGB.append(a)
            del a

        return tuple(RGB)

class Blended(type):
    def __new__( cls, obj, other, n ):
        log = getLogger(__name__)
        if n < 0 or n > 1:
            raise ValueError(f"'n' must be a value between 0 and 1")
        elif not all( isinstance( i, FG_Color|BG_Color|AnsiCombo ) for i in ( obj, other )):
            raise TypeError(f"Can't blend types '{type(obj).__name__}' and '{type(other).__name__}'")

        blend_val = n
        ext = {}
        code  = '_'.join([ c[:2] for c in ( 'blend', obj._code_, other._code_ )])

        objcolors, othercolors = getColors( obj, other )
        to_blend = [( objcolors[T], othercolors[T] ) for T in set(objcolors) & set(othercolors) ]

        log.debug(f"{obj = }, {other = }, {n = }")
        log.debug(f"{to_blend = }")
        if not to_blend:
            raise ValueError(f"No shared color types to blend {repr(obj)} and {repr(other)}")

    # Combo
        if isinstance( obj, AnsiCombo ):
            FG_names, BG_names = [], []
            # rgb_values = {}
            for A, B in to_blend:
                log.debug(f"Blending colors '{repr(A)}' and '{repr(B)}'")
                _blend = A.blend( B, n )
                objcolors.pop( type(A) )
                ext[ _blend.__name__ ] = _blend
                # names.append( _blend.name.split(' (')[0] )
                if isinstance( A, FG_Color ):
                    FG_names.append( cleanRep( _blend.__rep__, 'Blended' ))
                    # rgb_values['rgb'] = _blend.rgb
                else:
                    BG_names.append( cleanRep( _blend.__rep__, 'Blended' ))
                    # rgb_values['bg_rgb'] = _blend.rgb

                del _blend

            # if 'rgb' not in rgb_values:
                # rgb_values['rgb'] = rgb_values.pop('bg_rgb')

            b_name = ' & '.join([ '||'.join(FG_names), '||'.join(BG_names) ]) + f" -[ %{int(n*100)} ]"

            log.debug(f"Object to blend '{repr(obj)}' is type 'AnsiCombo'")


            styles = list(filter( lambda x: isinstance( x, Style ), obj.extended() ))
            ext = { **ext, **dict([( i.__name__, i ) for i in objcolors.values() ]), **dict([( i.__name__, i ) for i in styles ])}
            name = "AnsiCombo.Blended"
            _name = f"AnsiCombo: {' + '.join([ f'Blended( {b_name} )', *[ i.name for i in styles ] ])}"
            rep = f"AnsiCombo(< {' + '.join([ f'Blended( {b_name} )', *[ i.name for i in styles ] ])} >)"

            doc_lists = AnsiList( [ *obj.__doc__.split('\n'),
                                    *other.__doc__.split('\n'),
                                    *listFlatten([ i.__doc__.split('\n') for i in styles ]),
                                    ],
                                  strsep = '\n    ' )

            doc = f"{_name.replace('+','&')}\n    {doc_lists}"

            code = '_'.join([ *[ i._code_ for i in ext.values() ], 'blended' ])
            esc = ()
            html = {}
            for E in ext.values():
                esc += E.__esc__
                html = { **html, **E.__html__ }

            return type.__new__( AnsiCombo, name, (), { '_code_'     : code,
                                                        '__doc__'    : doc,
                                                        '__esc__'    : esc,
                                                        '__ext__'    : ext,
                                                        '__pre__'    : (),
                                                        '__rep__'    : rep,
                                                        '__html__'   : html,
                                                        'blend_value': blend_val,
                                                        'name'       : _name        })

    # Color
        elif isinstance( obj, FG_Color ):
            base_type = FG_Color
        elif isinstance( obj, BG_Color ):
            base_type = BG_Color
        else:
            raise TypeError(f"Type {type(obj)} can not be blended")

        A, B = to_blend[0]
        log.debug(f"Object to blend '{repr(obj)}' is type '{base_type}'")

        rgb = cls.__blend__( A, B, n )

        b_name = '||'.join([ cleanRep( A.__rep__, 'Blended' ), cleanRep( B.__rep__, 'Blended' ) ])
        _name = f"Blended: {b_name}"
        rep = f"Blended(< {b_name} >)"
        name = f"{obj.__name__}_{other.__name__}_blend"
        esc = obj.__pre__ + rgb

        if base_type == FG_Color:
            html = { 'color': f"rgb{rgb}" }
        else:
            html = { 'background-color': f"rgb{rgb}" }
        code = f"{A._code_}_{B._code_}_blend"

        doc = str(AnsiList([ f"Blended: {b_name}",
                             *[ f"    {i}" for i in obj.__doc__.split('\n') ],
                             *[ f"    {i}" for i in obj.__doc__.split('\n') ]],
                            strsep = '\n' ))

        R = type.__new__( base_type, name, (), { '_code_'     : code,
                                                 '__com__'    : obj.__com__,
                                                 '__doc__'    : doc,
                                                 '__esc__'    : esc,
                                                 '__ext__'    : ext,
                                                 '__html__'   : html,
                                                 '__pre__'    : obj.__pre__,
                                                 '__rep__'    : rep,
                                                 'bases'      : tuple( to_blend ),
                                                 'blend_value': blend_val,
                                                 'name'       : _name,
                                                 'rgb'        : rgb     })
        _setXtra_(R)
        return R

    def __blend__(a, b, n):
        from apputils import tupleCalc as tc
        if n == 1:
            return b.rgb
        elif n == 0:
            return a.rgb

        return tc( tc( a.rgb, 1-n, '*' ), tc( b.rgb, n, '*' ), '+', round_int = True )

class Inverted(type):
    def __new__( cls, obj ):
        ext = {}
        name = f"{obj.__name__}_inverted"

        colors = getColors( obj )
        b_name = cleanRep( ' + '.join([ i.__rep__ for i in colors.values() ]), 'Inverted' )

        name = f"{obj.__name__}_inverted"
        code = '_'.join([ i._code_ for i in colors ]) + '_inverted'

        if hasattr( obj, '__pre__' ):
            if obj.__pre__ == (38,2):
                rep = f"Inverted(< {_name} (Fg) >)"
                _name = f"{_name} (Inverted Fg)"
            else:
                rep = f"Inverted(< {_name} (Bg) >)"
                _name = f"{_name} (Inverted Bg)"
        else:
            rep = f"Inverted(< {_name} (AnsiCombo) >)"
            _name = f"{_name} (Inverted AnsiCombo)"

        code  = obj._code_+'_bright'

    # Combo
        if isinstance( obj, AnsiCombo ):

            html = {}
            rgb_values = {}
            s_names = []
            doc = ''
            for k, v in obj.__ext__.items():
                if not isinstance( v, FG_Color|BG_Color ):
                    nm, item = k, v
                    ext[nm] = item
                    s_names.append( cleanRep( item.__rep__ ))
                else:
                    item = v.invert()
                    nm = item.__name__
                    ext[nm] = item
                    rgb_values[ 'rgb' if isinstance( item, FG_Color ) else 'bg_rgb' ] = item.rgb

                if item.__com__:
                    doc += f"\n    - {item.__com__}"
                html = { **html, **item.__html__ }
                del nm, item

            if 'rgb' not in rgb_values:
                rgb_values['rgb'] = rgb_values.pop('bg_rgb')

            rep = f"AnsiCombo(< Inverted( {b_name} ) + {' + '.join(s_names)} >)"
            doc   = f"AnsiCombo: {b_name} & {' & '.join(s_names)}"

            esc = tuple( v.__esc__ for v in ext.values() )
            R = type.__new__( AnsiCombo, name, (), { '_code_'    : code,
                                                     '__doc__'     : doc,
                                                     '__esc__'     : esc,
                                                     '__ext__'     : ext,
                                                     '__pre__'     : (),
                                                     '__rep__'     : rep,
                                                     '__html__'    : html,
                                                     'name'        : _name   })
            _setXtra_(R)
            return R

    # Color
        elif isinstance( obj, FG_Color ):
            base_type = FG_Color
        elif isinstance( obj, BG_Color ):
            base_type = BG_Color
        else:
            raise TypeError(f"Type {type(obj)} can not be inverted")

        doc = f"Inverted: {obj.__doc__}"
        rgb = cls._inv_( cls, obj.rgb )
        esc = obj.__pre__ + rgb

        if base_type == FG_Color:
            html = { 'color': f"rgb{rgb}" }
        else:
            html = { 'background-color': f"rgb{rgb}" }

        R = type.__new__( base_type, name, (Inverted,), { '_code_'    : code,
                                                          '__com__'     : obj.__com__,
                                                          '__doc__'     : doc,
                                                          '__esc__'     : esc,
                                                          '__ext__'     : ext,
                                                          '__html__'    : html,
                                                          '__pre__'     : obj.__pre__,
                                                          '__rep__'     : rep,
                                                          'name'        : _name,
                                                          'revert'      : lambda: obj,
                                                          'rgb'         : rgb     })
        _setXtra_(R)
        return R

    def _inv_(self, rgb):
        from apputils import tupleCalc as tc
        RGB = []
        return tuple( abs( i - 255 ) for i in rgb )
