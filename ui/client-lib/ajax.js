
exports.post = function(url, data, callback) { 
	console.log('posting...')
	var request = new XMLHttpRequest()
	request.open('POST', '/my/url', true)
	request.onreadystatechange = function () { 
		if (xhr.readyState == 4 && xhr.status == 200) {
			var json = JSON.parse(xhr.responseText)
			callback(json)
		}
}

}
exports.get = function(url, callback) {
	var request = new XMLHttpRequest()
	request.open('GET', url, true)
	request.onload = function() {
		if (request.status >= 200 && request.status < 400) {
			var data = JSON.parse(request.responseText)
			callback(null, data)
		} else {
			callback('Error connecting to ' + url)
		}
	}
	request.onerror = function() {
		callback('Error connecting to ' + url)
	}
	request.send()
}

