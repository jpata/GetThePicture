var showPic = require('./pic')

module.exports = function(list) {
	createHTML(list, function(html) {
		document.getElementById('list').innerHTML = html
		$('.thumb').on('click', function(e) {
			showPic(e.target.id, list)
		})
	})
}

function createHTML(list, callback) {
	var html = ''
	list.forEach(function(l) {

		var item = '<h1>' + l.grade + '</h1>'
			+ '<p>File: ' + l.filename + '</p>'
			+ '<img class="thumb" id="' + l.filename + '" src="' + l.thumbnail + '"></img>'
		html = html + item
	})
	callback(html)
}


