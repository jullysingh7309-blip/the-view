require('dotenv').config({ path: __dirname + '/.env' });

var createError = require('http-errors');
var express = require('express');
var path = require('path');
var logger = require('morgan');
var app = express();
const exphbs  = require('express-handlebars');

var indexRouter = require('./routes/index');
var adminRouter = require('./routes/admin');
var loginRouter = require('./routes/login');

app.set('trust proxy', 1);

// View engine setup
app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'hbs');
app.engine('hbs', exphbs({
  defaultLayout: 'main',
  extname: '.hbs',
  partialsDir: __dirname + '/views/partials/'
}));

app.use(express.static(path.join(__dirname, 'assets')));
app.use(logger('dev'));
app.use(express.json());
app.use(express.urlencoded({ extended: false }));


app.use('/', indexRouter);
app.use('/', adminRouter);
app.use('/', loginRouter);

app.get('*', function(req, res){
  res.render('error')
});

// catch 404 and forward to error handler
app.use(function(req, res, next) {
  next(createError(404));
});

// Error handler
app.use(function(err, req, res, next) {
  res.locals.message = err.message;
  res.locals.error = req.app.get('env') === 'development' ? err : {};
  console.log(req.app.get('env'));
  res.status(err.status || 500);
  res.render('error');
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`✅ Public website running on http://localhost:${PORT}`);
});

module.exports = app;
