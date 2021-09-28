from .. import doc as d
from .. import convert
from .. import color as c

import inspect
import types

@convert.register(types.FunctionType.__repr__)
def convert_function(ctx, value):
	return convert.tagged(ctx,
		"function ",
		convert.identifier(ctx, value),
		_signature(ctx, value),
		convert.identity(ctx, value),
	)

@convert.register(types.MethodType.__repr__)
def convert_bound_method(ctx, value):
	return convert.tagged(ctx,
		"bound method ",
		convert.identifier(ctx, value),
		_signature(ctx, value),
		" of ", convert.convert(ctx, value.__self__),
	)

@convert.register(types.BuiltinFunctionType.__repr__)
def convert_builtin_function(ctx, value):
	return convert.tagged(ctx,
		"built-in function ",
		convert.identifier(ctx, value),
		_signature(ctx, value),
		d.Concat([
			" of ", convert.convert(ctx, value.__self__),
		]) if not isinstance(value.__self__, types.ModuleType) else d.NIL,
	)

@convert.register(types.MethodDescriptorType.__repr__)
def convert_method_descriptor(ctx, value):
	return convert.tagged(ctx,
		"method descriptor ",
		_name(ctx, value),
		_signature(ctx, value),
	)

@convert.register(types.ClassMethodDescriptorType.__repr__)
def convert_classmethod_descriptor(ctx, value):
	return convert.tagged(ctx,
		"class method descriptor ",
		_name(ctx, value),
		_signature(ctx, value),
	)

@convert.register(types.WrapperDescriptorType.__repr__)
def convert_wrapper_descriptor(ctx, value):
	return convert.tagged(ctx,
		"wrapper descriptor ",
		_name(ctx, value),
		_signature(ctx, value),
	)

@convert.register(types.GetSetDescriptorType.__repr__)
def convert_getset_descriptor(ctx, value):
	return convert.tagged(ctx,
		"attribute ",
		_name(ctx, value),
	)

@convert.register(types.MethodWrapperType.__repr__)
def convert_method_wrapper(ctx, value):
	return convert.tagged(ctx,
		"method wrapper ",
		_name(ctx, value),
		_signature(ctx, value),
		" of ", convert.convert(ctx, value.__self__),
	)

# _sitebuiltins
@convert.register(type(help).__repr__) # _sitebuiltins._Helper
def convert_sitebuiltins_helper(ctx, value):
	return convert.tagged(ctx, "function ", c.IDENTIFIER("help"), _signature(ctx, value))

@convert.register(type(quit).__repr__) # _sitebuiltins._Quitter
def convert_sitebuiltins_quitter(ctx, value):
	return convert.tagged(ctx, "function ", c.IDENTIFIER(value.name), _signature(ctx, value))

@convert.register(type(license).__repr__) # _sitebuiltins._Printer
def convert_sitebuiltins_printer(ctx, value):
	return convert.tagged(ctx, "function ", c.IDENTIFIER(value._Printer__name), _signature(ctx, value))

def _name(ctx, value):
	return c.IDENTIFIER(
		convert.moduleprefix(ctx, value.__objclass__)
		+ value.__objclass__.__qualname__
		+ "." + value.__name__
	)
...

def _signature(ctx, value):
	try:
		value = inspect.signature(value)
	except ValueError:
		return (c.RESET + c.FAINT)("(?)")

	P = inspect.Parameter
	result = []
	render_pos_only_separator = False
	render_kw_only_separator = True
	for param in value.parameters.values():
		if param.kind == P.POSITIONAL_ONLY:
			render_pos_only_separator = True
		elif render_pos_only_separator:
			result.append("/")
			render_pos_only_separator = False

		if param.kind == P.VAR_POSITIONAL:
			render_kw_only_separator = False
		elif param.kind == P.KEYWORD_ONLY and render_kw_only_separator:
			result.append("*")
			render_kw_only_separator = False

		item = [c.ARGUMENT(param.name)]
		if param.annotation is not P.empty:
			item.append(": ")
			item.append(convert.convert(ctx, param.annotation))
		if param.default is not P.empty:
			item.append("=" if param.annotation is P.empty else " = ")
			item.append(convert.convert(ctx, param.default))

		result.append(d.Concat(item))

	if render_pos_only_separator:
		result.append("/")

	rendered = convert.bracket(ctx, "(", result, ")")

	if value.return_annotation is not P.empty:
		rendered = d.Concat([
			rendered,
			" -> ",
			convert.convert(ctx, value.return_annotation)
		])

	return c.RESET(rendered)
