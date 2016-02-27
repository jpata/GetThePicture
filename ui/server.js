var express = require('express')
var app = express()
var bodyParser = require('body-parser')

app.use(bodyParser.urlencoded({ extended: false }))
app.use(bodyParser.json())

app.get('/', function(req, res) {
	res.sendFile(__dirname + '/public/index.html')
})

app.post('/test', function(req, res) {
	console.log(req.body)
	res.send({msg: 'received'})
})

var port = 3000
app.listen(port, function() {
	console.log('listening on port ' + port)
})
