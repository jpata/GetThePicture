var showList = require('./client-lib/list')

window.onload = function() {
	$('#path-btn').on('click', function() {
		var path = $('#path').val()
		$('#start').hide()
		$('#list').show()
		$('#list').html('<p>Analysing pictures...</p>')
		$.post('/test', {path: path}, function(list) {
			console.log(list)
			showList(list)
		})
	})
}
