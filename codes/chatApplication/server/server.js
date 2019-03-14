const express = require('express');
const mongoose = require('mongoose');
const cookieParser = require('cookie-parser');
const cors = require('cors');
//const logger = require('morgan');

const app = express();

app.use(cors());

const dbconfig = require('./config/secret');

app.use((req, res, next) => {
  res.header('Access-Control-Allow-Origin', '*');
  res.header('Access-Control-Allow-Credentials', 'true');
  res.header('Access-Control-Allow-Methods', 'GET', 'POST', 'DELETE', 'PUT');
  res.header('Access-Control-Allow-Headers', 'Origin, X-Requested-With, Content-Type, Accept');
  next();
});

app.use(express.json({ limit: '50mb' }));
app.use(express.urlencoded({ extended: true, limit: '50mb' }));
app.use(cookieParser());
//app.use(logger('dev'));

mongoose.Promise = global.Promise;
mongoose.connect(dbconfig.url, { useNewUrlParser: true });

const auth = require('./routes/authRoutes');

app.use('/api/artt', auth);

app.listen(3000, () => {
  console.log('Running on port 3000');
});
