const express = require('express');
const router = express.Router();
const fetch = require("node-fetch");
const request = require("request");
const https = require('https')

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

function checkAuth(req, res, next) {
    if (!req.session.admin){
        console.log("Session : ",req.session)
        console.log("Session Admin : ",req.session.admin)
        console.log("User ID : ",req.session.user_id)
        res.send('You are not authorized to view this page');
    } else {
        console.log("Session : ",req.session)
        console.log("Session Admin : ",req.session.admin)
        console.log("User ID : ",req.session.user_id)
        console.log('checkAuth Sucessful !!')
        next();
    }
}
/*

//////////////////////////////////////////
router.get('/addnews' ,  function(req, res, next) {

            res.render('admin-panel/add-news', {
                title_head: 'Admin - Add News',
                route: 'admin-trending-published',
                layout: 'admin.hbs'
            })

});



router.get('/admin-trending-published' ,  function(req, res, next) {

    getData('http://localhost:8080/getValueTrending')
        .then( output =>
            res.render('admin-panel/edit-published', {
                title_head: 'Admin - Trending',
                data: output,
                route: 'admin-trending-published',
                layout: 'admin.hbs'
            })
        )
});
router.get('/admin-technology-published' , function(req, res, next) {

    getData('http://localhost:8080/getAdminValueTechnologyPublished')
        .then( output =>
            res.render('admin-panel/edit', {
                title_head: 'Admin-Technology',
                data: output,
                route: 'admin-technology-published',
                layout: 'admin.hbs'
            })
        )
});
router.get('/admin-business-published'  , function(req, res, next) {

    getData('http://localhost:8080/getAdminValueBusinessPublished')
        .then( output =>
            res.render('admin-panel/edit', {
                title_head: 'Admin-Business',
                data: output,
                route: 'admin-business-published',
                layout: 'admin.hbs'
            })
        )
});
router.get('/admin-entertainment-published'  , function(req, res, next) {

    getData('http://localhost:8080/getAdminValueEntertainmentPublished')
        .then( output =>
            res.render('admin-panel/edit', {
                title_head: 'Admin-Entertainment',
                data: output,
                route: 'admin-entertainment-published',
                layout: 'admin.hbs'
            })
        )
});
router.get('/admin-health-published' , function(req, res, next) {

    getData('http://localhost:8080/getAdminValueHealthPublished')
        .then( output =>
            res.render('admin-panel/edit', {
                title_head: 'Admin-Health',
                data: output,
                route: 'admin-health-published',
                layout: 'admin.hbs'
            })
        )
});
router.get('/admin-sports-published' , function(req, res, next) {

    getData('http://localhost:8080/getAdminValueSportsPublished')
        .then( output =>
            res.render('admin-panel/edit', {
                title_head: 'Admin-Sports',
                data: output,
                route: 'admin-sports-published',
                layout: 'admin.hbs'
            })
        )
});



/!** DElETE NEWS Route *!/
router.post('/delete-news-entry-published', function(req,res,next) {

    let route = req.body.routeToRender;
    let urlToAPI = 'http://localhost:8080/v1/delete_news_published'

    let deleteData = JSON.stringify({
        id : req.body.idToDel
    })

    console.log(route);
    console.log(deleteData)


    let option_delete = {
        url: urlToAPI ,
        method: 'POST',
        json: deleteData
    };

    request(option_delete, function (error, response, body) {
        if (!error && response.statusCode == 200) {
            console.log("Delete completed") // Print the shortened url.
            res.redirect(route)
        }
        else {
            console.log("error: " + error)
            console.log("response.statusCode: " + response.statusCode)
            console.log("response.statusText: " + response.statusText)
            res.send(error)
        }
    });


});
/!* END Delete News Route *!/


/!* EDIT NEWS Route*!/


router.post('/update-entry-published', function(req,res,next) {

    let route = req.body.routeToRender;

    let newsData = JSON.stringify({
        publisher: req.body.publisher,
        title: req.body.title,
        description: req.body.description,
        urlToImage: req.body.urlToImage,
        category: req.body.category,
        publishedAt: req.body.publishedAt,
        createdAt: req.body.createdAt,
        hashtags: req.body.hashtags,
        sentiment: req.body.sentiment,
        url: req.body.url,
        id: req.body.idToEdit,
        desc_line: req.body.desc_line
    });
    console.log('NewsData: ', newsData);


    let options = {
        url: 'http://localhost:8080/v1/edit_news_story_published',
        method: 'POST',
        json: newsData
    };

    request(options, function (error, response, body) {
        if (!error && response.statusCode == 200) {
            console.log("Edit completed") // Print the shortened url.
            res.redirect(route)

        }
        else {

            console.log("error: " + error)
            console.log("response.statusCode: " + response.statusCode)
            console.log("response.statusText: " + response.statusText)
            res.send(error)
        }
    });



});



router.get('/admin-testing' ,  function(req, res, next) {

    getData('http://localhost:8080/getAdminTesting')
        .then( output =>
            res.render('admin-panel/edit', {
                title_head: 'Admin - Testing',
                data: output,
                route: 'admin-testing',
                layout: 'admin.hbs'
            })
        )
});


////////////////////////////////////
router.get('/admin-trending' ,  function(req, res, next) {

    getData('http://localhost:8080/getAdminValueTrending')
        .then( output =>
            res.render('admin-panel/edit', {
                title_head: 'Admin - Trending',
                data: output,
                route: 'admin-trending',
                layout: 'admin.hbs'
            })
        )
});
router.get('/admin-technology' , function(req, res, next) {

    getData('http://localhost:8080/getAdminValueTechnology')
        .then( output =>
            res.render('admin-panel/edit', {
                title_head: 'Admin-Technology',
                data: output,
                route: 'admin-technology',
                layout: 'admin.hbs',
                active_technology : 'yes'

            })
        )
});
router.get('/admin-business'  , function(req, res, next) {

    getData('http://localhost:8080/getAdminValueBusiness')
        .then( output =>
            res.render('admin-panel/edit', {
                title_head: 'Admin-Business',
                data: output,
                route: 'admin-business',
                layout: 'admin.hbs',
                active_business : 'yes'

            })
        )
});
router.get('/admin-entertainment'  , function(req, res, next) {

    getData('http://localhost:8080/getAdminValueEntertainment')
        .then( output =>
            res.render('admin-panel/edit', {
                title_head: 'Admin-Entertainment',
                data: output,
                route: 'admin-entertainment',
                layout: 'admin.hbs',
                active_entertainment : 'yes'

            })
        )
});
router.get('/admin-health' , function(req, res, next) {

    getData('http://localhost:8080/getAdminValueHealth')
        .then( output =>
            res.render('admin-panel/edit', {
                title_head: 'Admin-Health',
                data: output,
                route: 'admin-health',
                layout: 'admin.hbs',
                active_health : 'yes'

            })
        )
});
router.get('/admin-sports' , function(req, res, next) {

    getData('http://localhost:8080/getAdminValueSports')
        .then( output =>
            res.render('admin-panel/edit', {
                title_head: 'Admin-Sports',
                data: output,
                route: 'admin-sports',
                layout: 'admin.hbs',
                active_sports : 'yes'
            })
        )
});


/!** DElETE NEWS Route *!/
router.post('/delete-news-entry', function(req,res,next) {

    let route = req.body.routeToRender;
    let urlToAPI = 'http://localhost:8080/v1/delete_news'

    let deleteData = JSON.stringify({
        id : req.body.idToDel
    })
    console.log(route);
    console.log(deleteData)


    let option_delete = {
        url: urlToAPI ,
        method: 'POST',
        json: deleteData
    };

    request(option_delete, function (error, response, body) {
        if (!error && response.statusCode == 200) {
            console.log("Delete completed") // Print the shortened url.
            res.redirect(route)
        }
        else {

            console.log("error: " + error)
            console.log("response.statusCode: " + response.statusCode)
            console.log("response.statusText: " + response.statusText)
            res.send(error)
        }
    });


});
/!* END Delete News Route *!/


/!* EDIT NEWS Route*!/

router.post('/edit-news-entry', function(req,res,next) {
    let id = req.body.idToEdit;
    let route = req.body.routeToRender;
    res.redirect('/update' + route + '/' + id )

});


router.get('/update/:route/:id', function(req,res,next) {
    let idToEdit = req.params.id;
    console.log(idToEdit)

    let routeToRender = req.params.route;
    console.log(routeToRender)
    getData('http://localhost:8080/v1/edit_view?id=' + idToEdit)
        .then(output =>
            res.render('edit-page', {
                data: output,
                route: routeToRender
            })
        )

});


router.post('/update-entry', function(req,res,next) {

    let route = req.body.routeToRender;

    let newsData = JSON.stringify({
        publisher: req.body.publisher,
        title: req.body.title,
        description: req.body.description,
        urlToImage: req.body.urlToImage,
        category: req.body.category,
        publishedAt: req.body.publishedAt,
        createdAt: req.body.createdAt,
        hashtags: req.body.hashtags,
        sentiment: req.body.sentiment,
        url: req.body.url,
        id: req.body.idToEdit,
        desc_line: req.body.desc_line
    });
    console.log('NewsData: ', newsData);


    let options = {
        url: 'http://localhost:8080/v1/edit_news_story',
        method: 'POST',
        json: newsData
    };

    request(options, function (error, response, body) {
        if (!error && response.statusCode == 200) {
            console.log("Edit completed") // Print the shortened url.
            res.redirect(route)

        }
        else {

            console.log("error: " + error)
            console.log("response.statusCode: " + response.statusCode)
            console.log("response.statusText: " + response.statusText)
            res.send(error)
        }
    });



});




*/

module.exports = router;

