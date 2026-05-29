var express = require('express');
var createError = require('http-errors');
var router = express.Router();


router.get('/test', function(req, res){
    res.render('admin-panel/login',{
        layout: 'login.hbs'
    })
})


/*

router.get('/admin', function(req, res, next) {
    res.redirect("/admin-trending");
});
*/


/* GET users listing. */
/*
router.get('/admin', function(req, res, next) {
    console.log(req.session)
    res.render('login-page');
});
*/
router.post('/admin-login', function(req, res, next) {
    let email = req.body.email;
    let pass = req.body.password;


    console.log("email : ", email);
    console.log("password :", pass);

    if(email == 'admin@theview.live' && pass =='admin@1234'){
        console.log("Login Sucessful");
        req.session.user_id = 'admin@theview';
        req.session.admin = 'admin'
        res.redirect("/admin-trending")
    }
    else{
        console.log("Incorrect Login Credentials");
        next(createError(404));
        res.redirect('/test');
    }



});



module.exports = router;
