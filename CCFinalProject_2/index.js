import express from "express";
import bodyParser from "body-parser";
import pg from "pg";
import axios from 'axios';  // axios를 import로 불러옵니다.
import { OpenAI } from 'openai';
import dotenv from 'dotenv';

dotenv.config();  // .env 파일 로드

console.log(process.env.OPENAI_API_KEY);  // API 키 출력




const app = express();
const port = 3000;


app.set("view engine", "ejs");
app.use(express.urlencoded({ extended: true }));


const db = new pg.Client({
  user: "postgres",
  host: "localhost",
  database: "permalist",
  password: "claud9",
  port: 5432,
});
db.connect();

app.use(bodyParser.urlencoded({ extended: true }));
app.use(express.static("public"));

let items = [
  { id: 1, title: "Buy milk" },
  { id: 2, title: "Finish homework" },
];


app.get("/", async (req, res) => {
  const city = "Seoul"; // Default city
  const apiKey = "e668e22fda365ace6bab4579126bf50a"; // Your OpenWeatherMap API key
  const APIUrl = `https://api.openweathermap.org/data/2.5/weather?q=${city}&units=metric&appid=${apiKey}`;

  let weather;
  let error = null;
  
  try {
    const response = await axios.get(APIUrl);
    weather = response.data;
  } catch (err) {
    weather = null;
    error = "Error, Please try again";
  }


  res.render("index", { weather, error });
});


// 다른 날씨 보고싶을때 
app.get("/weather", async (req, res) => {
  const city = req.query.city  || "Seoul"; // 디폴트는 서울
  const apiKey = "e668e22fda365ace6bab4579126bf50a"; 
  const APIUrl = `https://api.openweathermap.org/data/2.5/weather?q=${city}&units=metric&appid=${apiKey}`;

  let weather;
  let error = null;
  
  try {
    const response = await axios.get(APIUrl);
    weather = response.data;
  } catch (err) {
    console.error(err.message); 
    weather = null;
    error = "Error, Please try again";
  }

 
  res.render("index", { weather, error });
});

// AI 채팅 요청 처리

app.post("/chat", async (req, res) => {
  const userMessage = req.body.message;

  // 메시지가 없거나 비어있으면 처리하지 않도록 예외 처리
  if (!userMessage || userMessage.trim() === "") {
    return res.status(400).send("Message content cannot be empty.");
  }

  try {
    // OpenAI API 호출
    const response = await openai.chat.completions.create({
      messages: [{ role: "user", content: userMessage }],
      model: "gpt-3.5-turbo", // 또는 gpt-3.5-turbo
    });

    const aiResponse = response.choices[0].message.content;

    // 사용자 메시지와 AI 응답을 클라이언트로 반환
    res.json({ userMessage, aiResponse });
  } catch (err) {
    console.error(err.message);
    res.status(500).send("Error with AI service");
  }
});


app.get("/admin", async (req, res) => {
  try {
    const result = await db.query("SELECT * FROM diaries ORDER BY id DESC");
    const diaries = result.rows;

    res.render("admin.ejs", { diaries: diaries }); // Pass 'diaries' to the view
  } catch (err) {
    console.log(err);
  }
});


app.get("/post", (req, res) => {
  res.render("post.ejs"); // admin.ejs 페이지를 렌더링합니다.
});

app.get("/login", (req, res) => {
  res.render("login.ejs"); // admin.ejs 페이지를 렌더링합니다.
});

///**  로그인 처리 부분 ,.,,,**////
// 로그인 처리
app.post("/login", async (req, res) => {
  const { email, password } = req.body;

  if (!email || !password) {
    return res.send("이메일과 비밀번호를 모두 입력해주세요.");
  }

  try {
    const result = await db.query("SELECT * FROM users WHERE email = $1", [email]);

    if (result.rows.length === 0) {
      return res.send("해당 이메일의 사용자가 없습니다.");
    }

    const user = result.rows[0];

    // 비밀번호를 DB에서 가져온 비밀번호와 비교
    if (user.password === password) {
      res.redirect("/"); 
    } else {
      res.send("비밀번호가 틀렸습니다.");
    }
  } catch (err) {
    console.error(err);
    res.send("로그인 처리 중 오류가 발생했습니다.");
  }
});


app.get("/register", (req, res) => {
  res.render("register.ejs"); // admin.ejs 페이지를 렌더링합니다.
});

app.post("/add", async (req, res) => {
  const { diaryTitle, diaryContent } = req.body;
  try {
    await db.query("INSERT INTO diaries (title, content) VALUES ($1, $2)", [diaryTitle, diaryContent]);
    console.log("?");
    res.render("index.ejs")
  } catch (err) {
    console.log(err);
  }
});

// 전체 포스트에서 포스트 삭제
app.post("/delete", async (req, res) => {
  const id = req.body.deleteItemId;  // 삭제할 포스트의 ID
  try {
    await db.query("DELETE FROM diaries WHERE id = $1", [id]);  // 데이터베이스에서 해당 포스트 삭제
    res.redirect("/admin");  // 삭제 후 admin 페이지로 리다이렉트
  } catch (err) {
    console.log(err);
  }
});



// 특정 포스트 보기 
app.get("/admin_detail/:id", async (req, res) => {
  const { id } = req.params; // 포스트 ID
  try {
    // 블로그 포스트 정보 가져오기
    const diaryResult = await db.query("SELECT * FROM diaries WHERE id = $1", [id]);
    const diary = diaryResult.rows[0]; // 특정 포스트의 정보

    // 댓글 정보 가져오기
    const commentsResult = await db.query("SELECT * FROM comments WHERE diary_id = $1 ORDER BY created_at DESC", [id]);
    const comments = commentsResult.rows; // 해당 포스트의 댓글들

    if (diary) {
      // admin_detail.ejs로 포스트 데이터와 댓글 데이터 전달
      res.render("admin_detail.ejs", { diary: diary, comments: comments });
    } else {
      res.status(404).send("Post not found");
    }
  } catch (err) {
    console.log(err);
    res.status(500).send("Server error");
  }
});


// 특정 포스트 댓글 추가
app.post('/api/comments/:diaryId', async (req, res) => {
  const diaryId = req.params.diaryId;
  const { author, content } = req.body;
  const createdAt = new Date(); // 현재 시간 설정

  try {
    // 댓글 데이터 저장
    await db.query(
      "INSERT INTO comments (diary_id, author, content, created_at) VALUES ($1, $2, $3, $4)", 
      [diaryId, author, content, createdAt]
    );

    // 댓글 추가 후 해당 블로그의 diaries 데이터 다시 불러오기
    const result = await db.query("SELECT * FROM diaries ORDER BY id DESC");
    res.redirect("/admin_detail/" + diaryId)
//    res.render('admin.ejs', { diaries: diaries }); // 댓글 추가 후 admin 페이지로 렌더링
  } catch (err) {
    console.log(err);
    res.status(500).send("Server error");
  }
});


// 특정 포스트 댓글 삭제
app.post("/delete/:diaryId/:commentId", async (req, res) => {
  const commentId = req.params.commentId;
  const diaryId = req.params.diaryId;
  try {
    console.log(`Deleting comment with ID: ${commentId}`);
    // DB에서 해당 댓글 삭제
    await db.query("DELETE FROM comments WHERE id = $1", [commentId]);
    
    res.redirect("/admin_detail/" + diaryId);
  } catch (err) {
    console.log(err);
    res.status(500).send("Server error");
  }
});


app.listen(port, () => {
  console.log(`Server running on port ${port}`);
});

