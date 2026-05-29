var express = require('express');
var router = express.Router();
const fetch = require("node-fetch");


const getData = async url => {
    let json;
    try {
        const response = await fetch(url);
        json = await response.json();
        console.log(json);
    }
    catch (error) {
        console.log(error);
    }
    return json;
};

/*

/!**************************************************************************!/



router.get('/v2-sports', function(req, res, next) {

    getData('https://firebase-flask-deploy-b7t6nyuila-uc.a.run.app/fetch_newsapi/sports')
        .then(response =>
            res.render('new-single', {
                title_head: 'Sports',
                data: response
            })
        )

});

router.get('/v2-technology', function(req, res, next) {

    getData('https://firebase-flask-deploy-b7t6nyuila-uc.a.run.app/fetch_newsapi/technology')
        .then(response =>
            res.render('new-single', {
                title_head: 'Technology',
                data: response
            })
        )

});



router.get('/v2-entertainment', function(req, res, next) {

    getData('https://firebase-flask-deploy-b7t6nyuila-uc.a.run.app/fetch_newsapi/entertainment')
        .then(response =>
            res.render('new-single', {
                title_head: 'Entertainment',
                data: response
            })
        )

});



router.get('/v2-business', function(req, res, next) {

    getData('https://firebase-flask-deploy-b7t6nyuila-uc.a.run.app/fetch_newsapi/business')
        .then(response =>
            res.render('new-single', {
                title_head: 'Business',
                data: response
            })
        )

});


router.get('/v2-health', function(req, res, next) {

    getData('https://firebase-flask-deploy-b7t6nyuila-uc.a.run.app/fetch_newsapi/health')
        .then(response =>
            res.render('new-single', {
                title_head: 'Health',
                data: response
            })
        )

});

router.get('/v2', function(req, res, next) {

    getData('https://firebase-flask-deploy-b7t6nyuila-uc.a.run.app/fetch_newsapi/general')
        .then(response =>
            res.render('new-single', {
                title_head: 'Trending',
                data: response
            })
        )

});




/!******************************************************************************************************************!/




router.get('/sports', function(req, res, next) {

    getData('https://firebase-flask-deploy-b7t6nyuila-uc.a.run.app/getValueSports')
        .then(response =>
            res.render('home', {
                title_head: 'VIEW - Sports',
                data: response[0],
                tags: response[1]
            })
        )

});

router.get('/technology', function(req, res, next) {

    getData('https://firebase-flask-deploy-b7t6nyuila-uc.a.run.app/getValueTechnology')
        .then(response =>
            res.render('home', {
                title_head: 'VIEW - Technology',
                data: response[0],
                tags: response[1]
            })
        )

});



router.get('/entertainment', function(req, res, next) {

    getData('https://firebase-flask-deploy-b7t6nyuila-uc.a.run.app/getValueEntertainment')
        .then(response =>
            res.render('home', {
                title_head: 'VIEW - Entertainment',
                data: response[0],
                tags: response[1]
            })
        )

});



router.get('/business', function(req, res, next) {

    getData('https://firebase-flask-deploy-b7t6nyuila-uc.a.run.app/getValueBusiness')
        .then(response =>
            res.render('home', {
                title_head: 'VIEW - Business',
                data: response[0],
                tags: response[1]
            })
        )

});


router.get('/health', function(req, res, next) {

    getData('https://firebase-flask-deploy-b7t6nyuila-uc.a.run.app/getValueHealth')
        .then(response =>
            res.render('home', {
                title_head: 'VIEW - Health',
                data: response[0],
                tags: response[1]
            })
        )

});

router.get('/', function(req, res, next) {

    getData('https://firebase-flask-deploy-b7t6nyuila-uc.a.run.app/getValueTrending')
        .then(response =>
            res.render('home', {
                title_head: 'VIEW - Trending',
                data: response[0],
                tags: response[1]
            })
        )

});

router.get('/getvideodata', function(req, res, next) {

    getData('http://127.0.0.1:5002/getVideo')
        .then(response =>
            res.render('video-content', {
                title_head: 'VIEW - Video',
                data: response
            })
        )

});


router.get('/hashtag/:tagName', function (req, res) {
    tag = req.params.tagName
    console.log(tag)
    getData('https://firebase-flask-deploy-b7t6nyuila-uc.a.run.app/v1/showtags?tagName=' + tag)
        .then(response =>
            res.render('hashtag_page', {
                title_head: 'VIEW - '+ tag,
                data: response[0],
                tags: response[1]
            })
        )
})

router.get('/description/:desc/:idname', function (req,res) {

    id = req.params.idname
    console.log(id)
    getData('https://firebase-flask-deploy-b7t6nyuila-uc.a.run.app/description?id=' + id)
        .then(response => {
            let newresponse = [];
            let newresponse2 = [];
            let i = 0;
            if (response[1].length >= 4) {
                for (; i < 4; i++) {
                    newresponse[i] = response[1][i]
                }
            }
            else{
                for (; i <response[1].length ; i++) {
                    newresponse[i] = response[1][i]
                }
            }
            for (; i <response[1].length ; i++) {
                newresponse2[i] = response[1][i]
            }

            console.log("New response: ",newresponse)
            console.log("New response 2: ",newresponse2)
            res.render('description_page', {
                title_head: 'VIEW',
                data: response[0],
                topcards: newresponse,
                cards: newresponse2,
                tags: response[2],
                layout: 'description.hbs'
            })}
        )

})



router.get('/search_hashtag', function(req, res) {

    getData('https://firebase-flask-deploy-b7t6nyuila-uc.a.run.app/searchtags')
        .then(response => {
                // Method to construct the json result set
                res.jsonp(response, {
                    'Content-Type': 'application/json'
                }, 200);
        });
});



*/
module.exports = router;

