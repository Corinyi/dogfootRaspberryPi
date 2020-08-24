var express = require('express')
var fs = require('fs')    // 파일 로드를 위한 모듈
var app = express()

app.locals.pretty = true
app.set('views', './view_file')
app.set('view engine', 'pug')
app.listen(3000, () => {
  console.log("Server has been started")
})

// 최상위 라우트로 접속 시 /hello로 리다이렉트 
app.get("/", (req, res) => {
  res.redirect('/hello')
})

app.get("/hello", (req, res) => {
  // html 파일 로드
  fs.readFile('test.html', (error, data) => {
    if(error) {
      console.log('error :'+error)
    }
    else {
      res.writeHead(200, {'ContentType':'text/html'})
      res.end(data)   // 응답 프로세스 종료 
    }
  })
})