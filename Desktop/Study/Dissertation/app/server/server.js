const express = require('express');
const mysql = require('mysql');
const cors = require('cors');
const bcrypt = require('bcryptjs');

const app = express();
app.use(cors({
  origin: '*', // Allow all origins
  methods: ['GET', 'POST', 'PUT', 'DELETE'], // Allow all methods
  allowedHeaders: ['Content-Type', 'Authorization'] // Allow specific headers
}));
app.use(express.json());

// MySQL Connection
const db = mysql.createConnection({
  host: 'localhost',
  user: 'root',
  password: '234236238',
  database: 'mobile_learning'
})

db.connect((err) => {
  if (err) {
    console.error('error connecting to database:', err);
    return;
  }
  console.log('connected to database');
});

app.post('/signup', async (req, res) => {
  try {
    const { username, email, password } = req.body;

    const salt = await bcrypt.genSalt(10);
    const hashedPassword = await bcrypt.hash(password, salt);

    const sql = "INSERT INTO user (username, email, password) VALUES (?, ?, ?)";
    const values = [username, email, hashedPassword];

    db.query(sql, values, (err, result) => {
      if (err) {
        console.error('Error inserting user:', err);
        return res.status(500).json({ error: 'Database error' });
      }
      console.log('User inserted:', result);
      return res.status(201).json({ message: 'User registered successfully' });
    });
  } catch (error) {
    console.error('Error during signup:', error);
    return res.status(400).json({ error: error.message });
  }
});

app.post('/login', (req, res) => {
  const { email, password } = req.body;
  const sql = "SELECT * FROM user WHERE `email` = ?";
  
  db.query(sql, [email], async (err, data) => {
    if (err) {
      console.error('Error during database query:', err);
      return res.status(500).json({ error: 'Database error' });
    }

    if (data.length === 0) {
      return res.json({ status: "Failed" });
    }

    const hashedPasswordFromDB = data[0].password;

    try {
      const passwordMatch = await bcrypt.compare(password, hashedPasswordFromDB);
      
      if (passwordMatch) {
        console.log('Login successful');
        return res.json({ status: "Success", user_id: data[0].id, username: data[0].username, email: data[0].email, img: data[0].img, type: data[0].type });
      } else {
        console.log('Login failed: Passwords do not match');
        return res.json({ status: "Failed" });
      }
    } catch (error) {
      console.error('Error comparing passwords:', error);
      return res.status(500).json({ error: 'Server error' });
    }
  });
});

app.put('/updateUser', async (req, res) => {
  const { username, email, password } = req.body;
  try {
    if (password) {
      // Hash the new password before updating
      const hashedPassword = await bcrypt.hash(password, 10);
      // Update user in the database with password
      const sql = "UPDATE user SET password = ? WHERE email = ?";
      const values = [hashedPassword, email];

      db.query(sql, values, (err, data) => {
        if (err) {
          console.error('Error during database query:', err);
          return res.status(500).json({ error: 'Database error' });
        }
        console.log('User password updated successfully');
        return res.status(200).json({ message: 'User password updated successfully' });
      });
    } else if (username) {
      // Update user in the database with username
      const sql = "UPDATE user SET username = ? WHERE email = ?";
      const values = [username, email];

      db.query(sql, values, (err, data) => {
        if (err) {
          console.error('Error during database query:', err);
          return res.status(500).json({ error: 'Database error' });
        }
        console.log('User username updated successfully');
        return res.status(200).json({ message: 'User username updated successfully' });
      });
    } else {
      return res.status(400).json({ error: 'Neither username nor password provided' });
    }
  } catch (error) {
    console.error('Error updating user:', error);
    return res.status(500).json({ error: 'Server error' });
  }
});

app.put('/updatePic', async (req, res) => {
  const { email: email, img: img } = req.body;
  const sql = "UPDATE user SET img = ? WHERE email = ?";
  const values = [img, email];

  db.query(sql, values, (err, data) => {
    if (err) {
      console.error('Error during database query:', err);
      return res.status(500).json({ error: 'Database error' });
    }
    console.log('User profile picture updated successfully');
    console.log(img, email)
    return res.status(200).json({ message: 'User picture updated successfully' });
  });
});

app.get('/getUser', async (req, res) => {
  const email = req.query.email;
  if (!email) {
    return res.status(400).json({ error: 'Email parameter is required' });
  }
  
  db.query('SELECT * FROM user WHERE email = ?', [email], (error, results) => {
    if (error) {
      console.error('Database query error:', error);
      return res.status(500).json({ error: 'Internal server error' });
    }
    
    if (results.length === 0) {
      return res.status(404).json({ error: 'User not found' });
    }
    console.log('result', results)
    res.json(results[0]);
  });
});


app.get('/categories', (req, res) => {
  db.query('SELECT * FROM categories', (error, results) => {
      if (error) throw error;
      res.send(results);
  });
});

app.get('/wordSet/:categoryId', (req, res) => {
  const categoryId = req.params.categoryId;
  db.query('SELECT * FROM word_sets WHERE category_id = ?', [categoryId], (error, results) => {
      if (error) throw error;
      res.send(results);
  });
});

app.get('/flashcards/:wordSetId', (req, res) => { // เดี๋ยวเปลี่ยนเป็น set ทีหลัง
  const wordSetId = req.params.wordSetId;
  db.query('SELECT * FROM flashcards WHERE word_set_id = ?', [wordSetId], (error, results) => {
      if (error) throw error;
      res.send(results);
  });
});

app.post('/game', (req, res) => {
  // Log the received request body
  console.log('Received data:', req.body);

  // Check if the combination of user_id and category_id already exists
  const checkQuery = "SELECT * FROM leaderboard WHERE user_id = ? AND word_set_id = ?";
  const checkValues = [req.body.user_id, req.body.word_set_id];

  db.query(checkQuery, checkValues, (err, result) => {
    if (err) {
      console.error('Error checking leaderboard:', err);
      return res.json("Error");
    }

    if (result.length > 0) {
      // Entry already exists, update finished_time
      const updateQuery = "UPDATE leaderboard SET finished_time = ? WHERE user_id = ? AND word_set_id = ?";
      const updateValues = [req.body.finished_time, req.body.user_id, req.body.word_set_id];

      db.query(updateQuery, updateValues, (err, updateResult) => {
        if (err) {
          console.error('Error updating leaderboard:', err);
          return res.json("Error");
        }
        console.log('Data updated:', updateResult);
        return res.json(updateResult);
      });
    } else {
      // Entry does not exist, insert new record
      const insertQuery = "INSERT INTO leaderboard (`user_id`, `word_set_id`, `finished_time`) VALUES (?, ?, ?)";
      const insertValues = [
        req.body.user_id,
        req.body.word_set_id,
        req.body.finished_time
      ];

      db.query(insertQuery, insertValues, (err, insertResult) => {
        if (err) {
          console.error('Error inserting into leaderboard:', err);
          return res.json("Error");
        }
        console.log('Data inserted:', insertResult);
        return res.json(insertResult);
      });
    }
  });
});

app.get('/leaderboard/:wordSetId', (req, res) => {
  const word_set_id = req.params.wordSetId;
  db.query(
    'SELECT @rank := @rank + 1 AS `rank`, img, u.username, l.finished_time \
    FROM leaderboard l \
    JOIN (SELECT @rank := 0) r \
    JOIN user u ON l.user_id = u.id \
    WHERE l.word_set_id = ? \
    ORDER BY l.finished_time ASC',
    [word_set_id],
    (error, results) => {
      if (error) {
        console.error('Error fetching leaderboard:', error);
        res.status(500).json({ error: 'Internal server error' });
      } else {
        res.status(200).json(results);
      }
    }
  );
});

app.listen(3000, ()=> {
  console.log("listening at port 3000")
});