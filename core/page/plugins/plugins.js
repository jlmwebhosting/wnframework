wn.pages['plugins'].onload = function(wrapper) { 
	wn.ui.make_app_page({
		parent: wrapper,
		title: 'Plugin Manager',
		single_column: true
	});
	
	wn.call({
		method:"webnotes.plugins.get_plugin_list",
		callback: function(r) {
			var $main = $(wrapper).find(".layout-main")
			if(!r.message.all.length) {
				$main.html('<div class="alert alert-info">No Plugins Installed</div>');
				return;
			}
			$main.empty();
			$.each(r.message.all, function(i, plugin) {
				$.extend(plugin, plugin.plugin_module_icon);
				$($r('<div style="border-bottom: 1px solid #c7c7c7; margin-bottom: 10px;">\
						<div style="float: left; width: 50px;">\
							<span style="padding: 10px; background-color: %(color)s; \
								border-radius: 5px; display: inline-block; ">\
								<i class="%(icon)s icon-fixed-width" \
									style="font-size: 30px; color: white; \
										text-align: center; padding-right: 0px;"></i>\
							</span>\
						</div>\
						<div style="margin-left: 70px;">\
							<div class="row">\
								<div class="col-xs-10">\
									<p><b>%(plugin_name)s</b></p>\
									<p class="text-muted">%(plugin_description)s\
										<br>Publisher: %(plugin_publisher)s; Version: %(plugin_version)s</p>\
								</div>\
								<div class="col-xs-2">\
									<button class="btn btn-info">Install</button></div>\
							</div>\
						</div>\
					</div>', plugin)).appendTo($main)
			})
		}
	})
}