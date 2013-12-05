# Copyright (c) 2013, Web Notes Technologies Pvt. Ltd. and Contributors
# MIT License. See license.txt 

from __future__ import unicode_literals

import webnotes, os, json
from webnotes.utils import get_base_path, get_path
			
def get_plugin_asset(group, asset_type, name):
	load_plugin_mapping()
	installed_plugins = get_installed_plugins()
	
	name = webnotes.scrub(name)
	
	asset = webnotes.plugin_cache[group][asset_type].get(name, False)
	
	if asset==False:
		if asset_type=="js":
			asset= ""
			if name in webnotes.plugin_mapping[group][asset_type]:
				plugin, asset_path = webnotes.plugin_mapping[group][asset_type][name]
				
				if plugin in installed_plugins:
					with open(os.path.join(get_path("plugins", asset_path)), "r") as asset_file:
						asset = asset_file.read()

		elif asset_type=="controller":
			asset = None
			if name in webnotes.plugin_mapping[group][asset_type]:
				plugin, asset_module = webnotes.plugin_mapping[group][asset_type][name]
				if plugin in installed_plugins:
					asset = webnotes.get_module(asset_module)
			else:
				asset = None
			
		webnotes.plugin_cache[group][asset_type][name] = asset
		
	return asset

def load_plugin_mapping():
	if not webnotes.plugin_mapping:
		webnotes.plugin_mapping = {
			"doctype":{"controller":{}, "js":{}}, 
			"report":{"controller":{}, "js":{}}
		}
		webnotes.plugin_cache = {
			"doctype": {
				"controller": {}
			}, 
			"report": {
				"js": {}, 
				"controller":{}
			}
		}
		webnotes.plugin_configs = {}
		plugins_path = get_path("plugins")
		group = None
		for basepath, folders, files in os.walk(get_path("plugins")):
			for dontwalk in ('locale', '.git', 'public'):
				if dontwalk in folders:
					folders.remove(dontwalk)
						
			for item in files:
				itempath = os.path.join(basepath, item)
				
				if item == "config.json":
					with open(itempath, 'r') as configjson:
						plugin_config = json.loads(configjson.read())
					plugin = plugin_config["plugin_name"]
					plugin_config["path"] = basepath
					webnotes.plugin_configs[plugin] = plugin_config
				
				group = os.path.split(basepath)[-1]
								
				if group in ('report', 'doctype'):
					if item.endswith(".js"):
						webnotes.plugin_mapping[group]["js"][item[:-3]] = (plugin, itempath)
			
					if item.endswith(".py") and not item.startswith("_"):
						webnotes.plugin_mapping[group]["controller"][item[:-3]] = (plugin, 
							os.path.relpath(itempath, get_path("plugins")).replace("/", ".")[:-3])
						
	return webnotes.plugin_mapping

def get_plugin_paths():
	plugin_paths = []
	from webnotes.utils import get_path
	plugins_path = get_path("plugins")
	for plugin in os.listdir(plugins_path):
		plugin_path =  os.path.join(plugins_path, plugin)
		if os.path.isdir(plugin_path):
			plugin_paths.append(plugin_path)
			
	return plugin_paths

def get_installed_plugins():
	def load_installed_plugins():
		return json.loads(webnotes.conn.get_global("installed_plugins") or "[]")
	return webnotes.cache().get_value("installed_plugins", load_installed_plugins)

def set_installed_plugins(plugins):
	webnotes.conn.set_global("installed_plugins", json.dumps(plugins))
	webnotes.clear_cache()
	
@webnotes.whitelist()
def install_plugin(plugin_name):
	webnotes.only_for("System Manager")
	
	plugins = get_installed_plugins()
	
	
	
	plugins.append(plugin_name)
	set_installed_plugins(plugins)

def clear_cache(doctype=None, docname=None):
	webnotes.plugin_mapping = None
	webnotes.plugin_cache = None
	webnotes.cache().delete_value("installed_plugins")
	
@webnotes.whitelist()
def get_plugin_list():
	webnotes.only_for("System Manager")
	load_plugin_mapping()
	plugin_list = webnotes.plugin_configs.values()
	plugin_list.sort(lambda a, b: a["plugin_name"] < b["plugin_name"])
	
	return {
		"all": plugin_list,
		"installed": get_installed_plugins()
	}
	
	
		
	