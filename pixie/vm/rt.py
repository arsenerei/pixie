__config__ = None
py_list = list
py_str = str
from rpython.rlib.objectmodel import specialize
from rpython.rtyper.lltypesystem import lltype, rffi
<<<<<<< HEAD
from pixie.vm.effects.effects import ArgList, raise_Ef, Continuation, answer_k, Object
from pixie.vm.effects.environment import Resolve
from pixie.vm.keyword import keyword
from rpython.rlib.rbigint import rbigint

from pixie.vm.effects.effect_transform import cps
from pixie.vm.code import munge
#import pixie.vm.stdlib



def wrap_fn(nm):
    kw_nm = keyword(unicode(nm))
    kw_ns = keyword(unicode("pixie.stdlib"))

    class ResolveResult(Continuation):
        _immutable_ = True
        def __init__(self, w_args):
            self._w_args = w_args

        def step(self, result):
            return result.invoke_Ef(self._w_args)

    def wrapper(*args):
        return raise_Ef(Resolve(kw_ns, kw_nm), ResolveResult(ArgList(py_list(args))))




    return wrapper


_inited_fns = ["first", "count", "list", "next", "-str", "-print"]

for x in _inited_fns:
    globals()[munge(x+"_Ef")] = wrap_fn(x)

_inited_vals = ["load-paths"]


def wrap_val(nm):
    kw_nm = keyword(unicode(nm))
    kw_ns = keyword(unicode("pixie.stdlib"))

    def wrapper():
        return raise_Ef(Resolve(kw_ns, kw_nm), answer_k)

    return wrapper

for x in _inited_vals:
    globals()[munge(x+"_Ef")] = wrap_val(x)
    
    
@specialize.argtype(0)
def wrap(x):
    if isinstance(x, bool):
        from pixie.vm.primitives import true, false
        return true if x else false
    if isinstance(x, int):
        from pixie.vm.numbers import Integer
        return Integer(x)
    if isinstance(x, rbigint):
        import pixie.vm.numbers as numbers
        return numbers.BigInteger(x)
    if isinstance(x, float):
        import pixie.vm.numbers as numbers
        return numbers.Float(x)
    if isinstance(x, unicode):
        from pixie.vm.string import String
        return String(x)
    if isinstance(x, py_str):
        from pixie.vm.string import String
        return String(unicode(x))
    if isinstance(x, Object):
        return x
    if x is None:
        from pixie.vm.primitives import nil
        return nil

    assert False, "Bad Wrap"



#
# def init():
#
#     import pixie.vm.code as code
#     from pixie.vm.object import affirm, _type_registry
#     from rpython.rlib.rarithmetic import r_uint, intmask
#     from rpython.rlib.rbigint import rbigint
#     from pixie.vm.primitives import nil, true, false
#     from pixie.vm.string import String
#     from pixie.vm.object import Object
#
#     _type_registry.set_registry(code._ns_registry)
#
#     def unwrap(fn):
#         if isinstance(fn, code.Var) and fn.is_defined() and hasattr(fn.deref(), "_returns"):
#             tp = fn.deref()._returns
#             if tp is bool:
#                 def wrapper(*args):
#                     ret = fn.invoke(py_list(args))
#                     if ret is nil or ret is false:
#                         return False
#                     return True
#                 return wrapper
#             elif tp is r_uint:
#                 return lambda *args: fn.invoke(py_list(args)).r_uint_val()
#             elif tp is unicode:
#                 def wrapper(*args):
#                     ret = fn.invoke(py_list(args))
#                     if ret is nil:
#                         return None
#                     affirm(isinstance(ret, String), u"Invalid return value, expected String")
#                     return ret._str
#                 return wrapper
#             else:
#                 assert False, "Don't know how to convert" + str(tp)
#         return lambda *args: fn.invoke(py_list(args))
#
#
#     if globals().has_key("__inited__"):
#         return
#
#     import sys
#     sys.setrecursionlimit(100000) # Yeah we blow the stack sometimes, we promise it's not a bug
#
#     import pixie.vm.numbers as numbers
#     import pixie.vm.bits as bits
#     from pixie.vm.code import wrap_fn
#     import pixie.vm.interpreter
#     import pixie.vm.stacklet as stacklet
#     import pixie.vm.atom
#     import pixie.vm.reduced
#     import pixie.vm.util
#     import pixie.vm.array
#     import pixie.vm.lazy_seq
#     import pixie.vm.persistent_list
#     import pixie.vm.persistent_hash_map
#     import pixie.vm.persistent_hash_set
#     import pixie.vm.custom_types
#     import pixie.vm.compiler as compiler
#     import pixie.vm.map_entry
#     import pixie.vm.reader as reader
#     import pixie.vm.libs.platform
#     import pixie.vm.libs.ffi
#     import pixie.vm.symbol
#     import pixie.vm.libs.path
#     import pixie.vm.libs.string
#
#
#
#     numbers.init()
#
#     @specialize.argtype(0)
#     def wrap(x):
#         if isinstance(x, bool):
#             return true if x else false
#         if isinstance(x, int):
#             return numbers.Integer(x)
#         if isinstance(x, rbigint):
#             return numbers.BigInteger(x)
#         if isinstance(x, float):
#             return numbers.Float(x)
#         if isinstance(x, unicode):
#             return String(x)
#         if isinstance(x, py_str):
#             return String(unicode(x))
#         if isinstance(x, Object):
#             return x
#         if x is None:
#             return nil
#
#         affirm(False, u"Bad wrap")
#
#     globals()["wrap"] = wrap
#
#
#     def int_val(x):
#         affirm(isinstance(x, numbers.Number), u"Expected number")
#         return x.int_val()
#
#     globals()["int_val"] = int_val
#
#     from pixie.vm.code import _ns_registry, BaseCode, munge
#
#     for name, var in _ns_registry._registry[u"pixie.stdlib"]._registry.iteritems():
#         name = munge(name)
#         print name
#         if isinstance(var.deref(), BaseCode):
#             globals()[name] = unwrap(var)
#         else:
#             globals()[name] = var
#
#
#     import pixie.vm.bootstrap
#
#     def reinit():
#         for name, var in _ns_registry._registry[u"pixie.stdlib"]._registry.iteritems():
#             name = munge(name)
#             if name in globals():
#                 continue
#
#             print "Found ->> ", name, var.deref()
#             if isinstance(var.deref(), BaseCode):
#                 globals()[name] = unwrap(var)
#             else:
#                 globals()[name] = var
#
#     #f = open("pixie/stdlib.lisp")
#     #data = f.read()
#     #f.close()
#     #rdr = reader.MetaDataReader(reader.StringReader(unicode(data)), u"pixie/stdlib.pixie")
#     #result = nil
#     #
#     # @wrap_fn
#     # def run_load_stdlib():
#     #     with compiler.with_ns(u"pixie.stdlib"):
#     #         while True:
#     #             form = reader.read(rdr, False)
#     #             if form is reader.eof:
#     #                 return result
#     #             result = compiler.compile(form).invoke([])
#     #             reinit()
#     #
#     # stacklet.with_stacklets(run_load_stdlib)
#
#
#     init_fns = [u"reduce", u"get", u"reset!", u"assoc", u"key", u"val", u"keys", u"vals", u"vec"]
#     for x in init_fns:
#         globals()[py_str(code.munge(x))] = unwrap(code.intern_var(u"pixie.stdlib", x))
#
#     init_vars = [u"load-paths"]
#     for x in init_vars:
#         globals()[py_str(code.munge(x))] = code.intern_var(u"pixie.stdlib", x)
#
#     globals()["__inited__"] = True
=======




def init():

    import pixie.vm.code as code
    from pixie.vm.object import affirm, _type_registry
    from rpython.rlib.rarithmetic import r_uint, intmask
    from rpython.rlib.rbigint import rbigint
    from pixie.vm.primitives import nil, true, false
    from pixie.vm.string import String
    from pixie.vm.object import Object

    _type_registry.set_registry(code._ns_registry)

    def unwrap(fn):
        if isinstance(fn, code.Var) and fn.is_defined() and hasattr(fn.deref(), "_returns"):
            tp = fn.deref()._returns
            if tp is bool:
                def wrapper(*args):
                    ret = fn.invoke(py_list(args))
                    if ret is nil or ret is false:
                        return False
                    return True
                return wrapper
            elif tp is r_uint:
                return lambda *args: fn.invoke(py_list(args)).r_uint_val()
            elif tp is unicode:
                def wrapper(*args):
                    ret = fn.invoke(py_list(args))
                    if ret is nil:
                        return None
                    affirm(isinstance(ret, String), u"Invalid return value, expected String")
                    return ret._str
                return wrapper
            else:
                assert False, "Don't know how to convert" + str(tp)
        return lambda *args: fn.invoke(py_list(args))


    if globals().has_key("__inited__"):
        return

    import sys
    sys.setrecursionlimit(100000) # Yeah we blow the stack sometimes, we promise it's not a bug

    import pixie.vm.numbers as numbers
    import pixie.vm.bits as bits
    from pixie.vm.code import wrap_fn
    import pixie.vm.interpreter
    import pixie.vm.stacklet as stacklet
    import pixie.vm.atom
    import pixie.vm.reduced
    import pixie.vm.util
    import pixie.vm.array
    import pixie.vm.lazy_seq
    import pixie.vm.persistent_list
    import pixie.vm.persistent_hash_map
    import pixie.vm.persistent_hash_set
    import pixie.vm.custom_types
    import pixie.vm.compiler as compiler
    import pixie.vm.map_entry
    import pixie.vm.reader as reader
    import pixie.vm.libs.platform
    import pixie.vm.libs.ffi
    import pixie.vm.symbol
    import pixie.vm.libs.path
    import pixie.vm.libs.string



    numbers.init()

    @specialize.argtype(0)
    def wrap(x):
        if isinstance(x, bool):
            return true if x else false
        if isinstance(x, int):
            return numbers.Integer(x)
        if isinstance(x, rbigint):
            return numbers.BigInteger(x)
        if isinstance(x, float):
            return numbers.Float(x)
        if isinstance(x, unicode):
            return String(x)
        if isinstance(x, py_str):
            return String(unicode(x))
        if isinstance(x, Object):
            return x
        if x is None:
            return nil

        affirm(False, u"Bad wrap")

    globals()["wrap"] = wrap


    def int_val(x):
        affirm(isinstance(x, numbers.Number), u"Expected number")
        return x.int_val()

    globals()["int_val"] = int_val

    from pixie.vm.code import _ns_registry, BaseCode, munge

    for name, var in _ns_registry._registry[u"pixie.stdlib"]._registry.iteritems():
        name = munge(name)
        print name
        if isinstance(var.deref(), BaseCode):
            globals()[name] = unwrap(var)
        else:
            globals()[name] = var


    import pixie.vm.bootstrap

    def reinit():
        for name, var in _ns_registry._registry[u"pixie.stdlib"]._registry.iteritems():
            name = munge(name)
            if name in globals():
                continue

            print "Found ->> ", name, var.deref()
            if isinstance(var.deref(), BaseCode):
                globals()[name] = unwrap(var)
            else:
                globals()[name] = var

    #f = open("pixie/stdlib.pxi")
    #data = f.read()
    #f.close()
    #rdr = reader.MetaDataReader(reader.StringReader(unicode(data)), u"pixie/stdlib.pixie")
    #result = nil
    #
    # @wrap_fn
    # def run_load_stdlib():
    #     with compiler.with_ns(u"pixie.stdlib"):
    #         while True:
    #             form = reader.read(rdr, False)
    #             if form is reader.eof:
    #                 return result
    #             result = compiler.compile(form).invoke([])
    #             reinit()
    #
    # stacklet.with_stacklets(run_load_stdlib)


    init_fns = [u"reduce", u"get", u"reset!", u"assoc", u"key", u"val", u"keys", u"vals", u"vec"]
    for x in init_fns:
        globals()[py_str(code.munge(x))] = unwrap(code.intern_var(u"pixie.stdlib", x))

    init_vars = [u"load-paths"]
    for x in init_vars:
        globals()[py_str(code.munge(x))] = code.intern_var(u"pixie.stdlib", x)

    globals()["__inited__"] = True
>>>>>>> master






