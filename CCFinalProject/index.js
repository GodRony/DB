import express from "express";
import bodyParser from "body-parser";
import pg from "pg";

const app = express();
const port = 3000;

app.set("view engine", "ejs");

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
  try {
    const result = await db.query("SELECT * FROM items ORDER BY id ASC");
    items = result.rows;

    res.render("index.ejs", {
      listTitle: "Today",
      listItems: items,
    });
  } catch (err) {
    console.log(err);
  }
});

app.post("/add", async (req, res) => {
  const item = req.body.newItem;
  // items.push({title: item});
  try {
    await db.query("INSERT INTO items (title) VALUES ($1)", [item]);
    res.redirect("/");
  } catch (err) {
    console.log(err);
  }
});

app.post("/edit", async (req, res) => {
  const item = req.body.updatedItemTitle;
  const id = req.body.updatedItemId;

  try {
    await db.query("UPDATE items SET title = ($1) WHERE id = $2", [item, id]);
    res.redirect("/");
  } catch (err) {
    console.log(err);
  }
});

app.post("/delete", async (req, res) => {
  const id = req.body.deleteItemId;
  try {
    await db.query("DELETE FROM items WHERE id = $1", [id]);
    res.redirect("/");
  } catch (err) {
    console.log(err);
  }
});

app.listen(port, () => {
  console.log(`Server running on port ${port}`);
});

// index.js (서버 코드) 다이어리에관해
app.get("/diary", async (req, res) => {
  try {
    const result = await db.query("SELECT * FROM diaries ORDER BY id DESC");
    const diaries = result.rows;

    res.render("diaries.ejs", {
      diaries: diaries,
    });
  } catch (err) {
    console.log(err);
  }
});

app.post("/diary/add", async (req, res) => {
  const { diaryTitle, diaryContent } = req.body;
  
  try {
    await db.query("INSERT INTO diaries (title, content) VALUES ($1, $2)", [diaryTitle, diaryContent]);
    res.redirect("/diary");
  } catch (err) {
    console.log(err);
  }
});
