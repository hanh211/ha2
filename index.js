const express=require('express');

const app=express();
const server=require("http").Server(app);
app.use(express.static("public"))
const port=3000;

app.set("view engine","ejs");
app.engine('html',require('ejs').renderFile);
const io=require("socket.io")(server);

var mangUser=[];

io.on("connection",(socket)=>{
  console.log("co nguoi ket noi");
  socket.on("client-sen-txtUsername",(data)=>{
    if(mangUser.indexOf(data)>=0){
      socket.emit("server-send-dki-thatbai")
    }else{
      mangUser.push(data);
      socket.Username=data;
      socket.emit("server-send-dky-thanhcong",data);
      io.sockets.emit("server-send-danhsach-Users",mangUser);
    }
  });
  socket.on("logout",()=>{
    mangUser.splice(
      mangUser.indexOf(socket.Username),1
    );
    socket.broadcast.emit("server-send-danhsach-Users",mangUser);
  });
  socket.on("user-send-message",(data)=>{
    io.sockets.emit("server-send-message",{un:socket.Username,nd:data});
  });
  socket.on("toi-dang-go-chu",()=>{
    var s=socket.Username+"dang go chu";
    io.sockets.emit("ai-do-dang-go-chu",s);
  });
  socket.on("toi-stop-go-chu",()=>{
    var s1=socket.Username+"ngung go chu";
    io.sockets.emit("ai-do-stop-go-chu",s1);
  });
});


app.get('/',(req,res)=>{
  res.render('index.html')
});

server.listen(port,()=>{
  console.log('listen 3000')
});
