var express = require('express')
var app = express()
var bodyParser = require('body-parser')

app.use(bodyParser.urlencoded({ extended: false }))
app.use(bodyParser.json())

app.get('/', function(req, res) {
	res.sendFile(__dirname + '/public/index.html')
})
app.get('/script.js', function(req, res) {
	res.sendFile(__dirname + '/public/script.js')
})


var list = [
	{
		filename: 'Filename',
		thumbnail: '/photo/1.png',
		grade: 1
	},
	{
		filename: 'Filename',
		thumbnail: '/photo/1.png',
		grade: 0.5
	},
	{
		filename: 'Filename',
		thumbnail: '/photo/1.png',
		grade: 0.2
	}
]


app.post('/test', function(req, res) {
	console.log(req.body)
	res.send(list)
})

var port = 3000
app.listen(port, function() {
	console.log('listening on port ' + port)
})
