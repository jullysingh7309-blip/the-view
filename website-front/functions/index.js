var createError = require('http-errors');
var express = require('express');
var path = require('path');
var expressSession = require('express-session');
const FirebaseStore = require('connect-session-firebase')(expressSession);
const admin = require('firebase-admin');
var logger = require('morgan');
const functions = require('firebase-functions');
var app = express();
const exphbs  = require('express-handlebars');
let serviceAccount = require("./serviceAccount.json");

var indexRouter = require('./routes/index');
var adminRouter = require('./routes/admin');
var loginRouter = require('./routes/login');

try {
  const ref = admin.initializeApp({
    credential: admin.credential.cert(serviceAccount),
    databaseURL: "https://theview-c065c.firebaseio.com"
  });
  global.ref = ref;
} catch(e) {
  console.warn("⚠️  Firebase initialization skipped:", e.message);
  console.warn("⚠️  Running in local development mode");
  global.ref = null;
}

app.set('trust proxy', 1); // trust first proxy

// view engine setup
app.set('views', path.join(__dirname, 'views'));

app.set('view engine', 'hbs');
app.engine('hbs', exphbs({
  defaultLayout: 'main.hbs',
  partialsDir: __dirname + '/views/partials/'
}));


app.use(express.static(path.join(__dirname, 'assets')));
// view engine setup


app.use(logger('dev'));
app.use(express.json());
app.use(express.urlencoded({ extended: false }));

let sessionConfig = {
  resave: false,
  saveUninitialized: true,
  secret: 'ssshhhhh',
  cookie: {
    maxAge: 8*60*60*1000,
  },
};

if (global.ref) {
  sessionConfig.store = new FirebaseStore({
    database: global.ref.database()
  });
}

app.use(expressSession(sessionConfig));


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

// error handler
app.use(function(err, req, res, next) {
  // set locals, only providing error in development
  res.locals.message = err.message;
  console.log(err.message)
  res.locals.error = req.app.get('env') === 'development' ? err : {};
console.log(req.app.get('env'))
  // render the error page
  res.status(err.status || 500);
  res.render('error');
});


exports.app = functions.https.onRequest(app);

// Local development server
if (process.env.NODE_ENV === 'development' || !process.env.FUNCTION_NAME) {
  const PORT = process.env.PORT || 3000;
  app.listen(PORT, () => {
    console.log(`✅ Public website running on http://localhost:${PORT}`);
  });
}
