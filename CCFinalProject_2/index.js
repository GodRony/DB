import express from "express";
import bodyParser from "body-parser";
import pg from "pg";

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
    res.render("index.ejs");
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


app.listen(port, () => {
  console.log(`Server running on port ${port}`);
});

