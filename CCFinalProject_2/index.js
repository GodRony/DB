import express from "express";
import bodyParser from "body-parser";
import pg from "pg";
import axios from 'axios';  // axios를 import로 불러옵니다.

axios.get('https://api.example.com/data')
  .then(response => {
    console.log(response.data);
  })
  .catch(error => {
    console.log('Error:', error);
  });



const app = express();
const port = 3000;


app.set("view engine", "ejs");
app.use(express.urlencoded({ extended: true }));


const db = new pg.Client({
  user: "postgres",
  host: "localhost",
  database: "permalist",
  password: "",
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

  // Render the index template with the weather data and error message
  res.render("index", { weather, error });
});


// Handle the /weather route
app.get("/weather", async (req, res) => {
  const city = req.query.city  || "Seoul"; // Default city
  const apiKey = "e668e22fda365ace6bab4579126bf50a"; // Your OpenWeatherMap API key
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

  // Render the index template with the weather data and error message
  res.render("index", { weather, error });
});


// Render the index template with the weather data and error message



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


app.post("/delete", async (req, res) => {
  const id = req.body.deleteItemId;  // 삭제할 포스트의 ID
  try {
    await db.query("DELETE FROM diaries WHERE id = $1", [id]);  // 데이터베이스에서 해당 포스트 삭제
    res.redirect("/admin");  // 삭제 후 admin 페이지로 리다이렉트
  } catch (err) {
    console.log(err);
  }
});

//////////

// 특정 포스트의 상세 페이지 라우터
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


// 댓글 추가
// 댓글 추가
app.post('/api/comments/:blogId', async (req, res) => {
  const blogId = req.params.blogId;
  const { author, content } = req.body;
  const createdAt = new Date(); // 현재 시간 설정

  try {
    // 댓글 데이터 저장
    await db.query(
      "INSERT INTO comments (diary_id, author, content, created_at) VALUES ($1, $2, $3, $4)", 
      [blogId, author, content, createdAt]
    );

    // 댓글 추가 후 해당 블로그의 diaries 데이터 다시 불러오기
    const result = await db.query("SELECT * FROM diaries ORDER BY id DESC");
    const diaries = result.rows;

    // admin.ejs로 diaries를 전달
    res.render('admin.ejs', { diaries: diaries }); // 댓글 추가 후 admin 페이지로 렌더링
  } catch (err) {
    console.log(err);
    res.status(500).send("Server error");
  }
});





app.listen(port, () => {
  console.log(`Server running on port ${port}`);
});

