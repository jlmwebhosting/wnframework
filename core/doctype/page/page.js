// Copyright (c) 2013, Web Notes Technologies Pvt. Ltd. and Contributors
// MIT License. See license.txt 

cur_frm.cscript.refresh = function(doc, cdt, cdn) {
	cur_frm.set_df_property("plugin", "read_only", !!!doc.__islocal);
	cur_frm.cscript.standard(doc);
}
cur_frm.cscript.standard = function(doc) { 
	cur_frm.set_df_property("plugin", "reqd", doc.standard==="No");
}