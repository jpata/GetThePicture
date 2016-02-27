(function e(t,n,r){function s(o,u){if(!n[o]){if(!t[o]){var a=typeof require=="function"&&require;if(!u&&a)return a(o,!0);if(i)return i(o,!0);var f=new Error("Cannot find module '"+o+"'");throw f.code="MODULE_NOT_FOUND",f}var l=n[o]={exports:{}};t[o][0].call(l.exports,function(e){var n=t[o][1][e];return s(n?n:e)},l,l.exports,e,t,n,r)}return n[o].exports}var i=typeof require=="function"&&require;for(var o=0;o<r.length;o++)s(r[o]);return s})({1:[function(require,module,exports){
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



},{"./pic":2}],2:[function(require,module,exports){
module.exports = function(src) {
	$('#list').hide()
	$('#pic').html('<img src="' + src + '"><br><button id="back">Back to list</button>')
	$('#pic').show()
	$('#back').on('click', function() {
		$('#list').show()
	}) 
}

},{}],3:[function(require,module,exports){
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

},{"./client-lib/list":1}]},{},[3]);
