const server=require('express');
const bodyParser=require('body-parser');
const {spawn}=require('child_process');
const app=server();
const port=3000;
app.set("view engine","ejs");
app.engine('html',require('ejs').renderFile);
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({extended:false}));

app.get('/',(req,res)=>{
  res.render('a.html')
});

app.get('/a',(req,res)=>{
  var pythoncapitalfimer=spawn('python',['a.py',req.body.country]);
  pythoncapitalfimer.stdout.on('data',function(data){
    // console.log(datatoSend);
    datatoSend=data.toString();
  });
  pythoncapitalfimer.on('close',(code)=>{
    console.log(`chao ${code}`);
    // console.log(datatoSend);
    res.json({
      capital:datatoSend
    });
  });
});


app.listen(port,()=>{
  console.log('listen 3000')
});
