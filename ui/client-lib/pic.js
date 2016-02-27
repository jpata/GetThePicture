module.exports = function(src) {
	$('#list').hide()
	$('#pic').html('<img src="' + src + '"><br><button id="back">Back to list</button>')
	$('#pic').show()
	$('#back').on('click', function() {
		$('#list').show()
	}) 
}
