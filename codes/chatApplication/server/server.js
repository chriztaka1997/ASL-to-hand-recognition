const express = require('express');
const mongoose = require('mongoose');
const cookieParser = require('cookie-parser');
//const logger = require('morgan');

const app = express();
const dbconfig = require('./config/secret');

app.use(express.json({limit: '50mb'}));
app.use(express.urlencoded({extended: true, limit: '50mb'}))
app.use(cookieParser());
//app.use(logger('dev'));

mongoose.Promise = global.Promise;
mongoose.connect(dbconfig.url, { useNewUrlParser: true });

const auth = require('./routes/authRoutes');

app.use('/api/artt', auth);

app.listen(4200, () => {
  console.log('Running on port 27017');
});
