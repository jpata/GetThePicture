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
app.get('/photo/1.png', function(req, res) {
	res.sendFile(__dirname + '/public/troll.png')
})

var list = [
	{
		filename: '/photo/1.png',
		thumbnail: '/photo/1.png',
		grade: 1
	},
	{
		filename: '/photo/1.png',
		thumbnail: '/photo/1.png',
		grade: 0.5
	},
	{
		filename: '/photo/1.png',
		thumbnail: '/photo/1.png',
		grade: 0.555
	},
	{
		filename: '/photo/1.png',
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
