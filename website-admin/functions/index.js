require('dotenv').config({ path: __dirname + '/.env' });

var createError = require('http-errors');
var express = require('express');
var path = require('path');
var cors = require('cors');
var logger = require('morgan');
const fetch = require("node-fetch");
var bodyParser = require('body-parser');
const cookieParser = require("cookie-parser");
const { engine: hbsEngine } = require('express-handlebars');
const app = express();

var indexRouter = require('./routes');
var adminRouter = require('./routes/admin');
var loginRouter = require('./routes/login');

app.set('trust proxy', 1);

// View engine setup
app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'hbs');
app.engine('hbs', hbsEngine({
  defaultLayout: 'main',
  extname: '.hbs',
  partialsDir: __dirname + '/views/partials/'
}));

app.use(cors({
  origin: process.env.NODE_ENV === "production"
    ? process.env.CLIENT_URL
    : "http://localhost:3000",
  credentials: true
}));

app.use(express.static(path.join(__dirname, 'assets')));
app.use(bodyParser.urlencoded({ extended: false }));
app.use(bodyParser.json());
app.use(cookieParser());
app.use(logger('dev'));
app.use(express.json());
app.use(express.urlencoded({ extended: false }));

app.use('/', indexRouter);
app.use('/', adminRouter);
app.use('/', loginRouter);

// catch 404
app.use(function (req, res, next) {
  next(createError(404));
});

// error handler
app.use(function (err, req, res, next) {
  res.locals.message = err.message;
  res.locals.error = req.app.get('env') === 'development' ? err : {};
  console.log(req.app.get('env'));
  res.status(err.status || 500);
  res.render('error');
});

const PORT = process.env.PORT || 3001;
app.listen(PORT, () => {
  console.log(`✅ Admin panel running on http://localhost:${PORT}`);
});

module.exports = app;
