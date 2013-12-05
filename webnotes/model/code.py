# Copyright (c) 2013, Web Notes Technologies Pvt. Ltd. and Contributors
# MIT License. See license.txt 

from __future__ import unicode_literals

import webnotes
import webnotes.model.doc
from webnotes.modules import scrub

def get_obj(dt = None, dn = None, doc=None, doclist=[], with_children = 0):
	if dt:
		if isinstance(dt, list):
			return get_server_obj(dt[0], dt)
		if isinstance(dt, webnotes.model.doc.Document):
			return get_server_obj(dt, [dt])
		if not dn:
			dn = dt
		if with_children:
			doclist = webnotes.model.doc.get(dt, dn, from_controller=1)
		else:
			doclist = webnotes.model.doc.get(dt, dn, with_children = 0, from_controller=1)
		return get_server_obj(doclist[0], doclist)
	else:
		return get_server_obj(doc, doclist)

def get_server_obj(doc, doclist = [], basedoctype = ''):
	# for test
	from webnotes.plugins import get_plugin_asset
		
	DocType = get_doctype_class(doc.doctype)
	
	if webnotes.flags.in_import:
		return DocType(doc, doclist)

	# custom?
	plugin_controller = get_plugin_asset("doctype", "controller", doc.doctype)
	if plugin_controller:
		return plugin_controller.CustomDocType(doc, doclist)
	else:
		return DocType(doc, doclist)

def get_doctype_class(doctype):
	module = load_doctype_module(doctype)
	if module:
		DocType = getattr(module, 'DocType')
	else:
		if not cint(webnotes.conn.get_value("DocType", doctype, "custom")):
			raise ImportError, "Unable to load module for: " + doctype
		
	return DocType

def load_doctype_module(doctype, prefix=""):
	try:
		module = __import__(get_module_name(doctype, prefix), fromlist=[''])
		return module
	except ImportError, e:
		# webnotes.errprint(webnotes.getTraceback())
		return None

doctype_modules = {}

def get_module_name(doctype, prefix):
	if not doctype in doctype_modules:
		plugin, module = webnotes.conn.get_value("DocType", doctype, ["plugin", "module"])
		doctype_modules[doctype] = (webnotes.scrub(plugin), webnotes.scrub(module))
	
	plugin, module = doctype_modules[doctype]
	doctype = webnotes.scrub(doctype)

	name = '%s.doctype.%s.%s%s' % (module, doctype, prefix, doctype)
	if plugin:
		name = plugin + "." + name
	return name

def run_server_obj(server_obj, method_name, arg=None):
	if server_obj and hasattr(server_obj, method_name):
		if arg:
			return getattr(server_obj, method_name)(arg)
		else:
			return getattr(server_obj, method_name)()
	else:
		raise Exception, 'No method %s' % method_name
