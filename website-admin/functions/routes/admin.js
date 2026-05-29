const express = require('express');
const router = express.Router();
const fetch = require("node-fetch");
const request = require("request");

const API_URL = process.env.API_URL || 'http://localhost:8080';
const SUPABASE_URL = process.env.SUPABASE_URL || '';
const SUPABASE_SERVICE_KEY = process.env.SUPABASE_SERVICE_KEY || '';

const getData = async url => {
    let json;
    try {
        const response = await fetch(url);
        json = await response.json();
    } catch (error) {
        console.log('getData error:', error.message);
    }
    return json;
};

// Auth check via direct HTTP (no WebSocket needed)
async function checkAuth(req, res, next) {
    const sessionCookie = req.cookies.session || "";
    try {
        const resp = await fetch(`${SUPABASE_URL}/auth/v1/user`, {
            headers: {
                'Authorization': `Bearer ${sessionCookie}`,
                'apikey': SUPABASE_SERVICE_KEY
            }
        });
        if (resp.status !== 200) return res.redirect("/login");
        next();
    } catch (e) {
        return res.redirect("/login");
    }
}

//////////////////////////////////////////

router.get('/pdRnZRfiUaSx2cAcLdK5/add-news', function (req, res, next) {
    res.render('admin-panel/addnews', {
        title_head: 'Admin - Add news',
        route: 'pdRnZRfiUaSx2cAcLdK5/add-news',
        layout: 'admin.hbs'
    });
});

router.get('/pdRnZRfiUaSx2cAcLdK5/add-news-link', function (req, res, next) {
    res.render('admin-panel/addnews-link', {
        title_head: 'Admin - Add news Link',
        route: 'pdRnZRfiUaSx2cAcLdK5/add-news-link',
        layout: 'admin.hbs'
    });
});

router.get('/pdRnZRfiUaSx2cAcLdK5/admin-trending-published', function (req, res, next) {
    getData(`${API_URL}/getAdminValueTrendingPublished`)
        .then(output => res.render('admin-panel/edit-published', {
            title_head: 'Admin - Trending',
            data: output,
            route: 'pdRnZRfiUaSx2cAcLdK5/admin-trending-published',
            layout: 'admin.hbs'
        }));
});

router.get('/pdRnZRfiUaSx2cAcLdK5/admin-technology-published', function (req, res, next) {
    getData(`${API_URL}/getAdminValueTechnologyPublished`)
        .then(output => res.render('admin-panel/edit-published', {
            title_head: 'Admin-Technology',
            data: output,
            route: 'pdRnZRfiUaSx2cAcLdK5/admin-technology-published',
            layout: 'admin.hbs'
        }));
});

router.get('/pdRnZRfiUaSx2cAcLdK5/admin-business-published', function (req, res, next) {
    getData(`${API_URL}/getAdminValueBusinessPublished`)
        .then(output => res.render('admin-panel/edit-published', {
            title_head: 'Admin-Business',
            data: output,
            route: 'pdRnZRfiUaSx2cAcLdK5/admin-business-published',
            layout: 'admin.hbs'
        }));
});

router.get('/pdRnZRfiUaSx2cAcLdK5/admin-entertainment-published', function (req, res, next) {
    getData(`${API_URL}/getAdminValueEntertainmentPublished`)
        .then(output => res.render('admin-panel/edit', {
            title_head: 'Admin-Entertainment',
            data: output,
            route: 'pdRnZRfiUaSx2cAcLdK5/admin-entertainment-published',
            layout: 'admin.hbs'
        }));
});

router.get('/pdRnZRfiUaSx2cAcLdK5/admin-health-published', function (req, res, next) {
    getData(`${API_URL}/getAdminValueHealthPublished`)
        .then(output => res.render('admin-panel/edit', {
            title_head: 'Admin-Health',
            data: output,
            route: 'pdRnZRfiUaSx2cAcLdK5/admin-health-published',
            layout: 'admin.hbs'
        }));
});

router.get('/pdRnZRfiUaSx2cAcLdK5/admin-sports-published', function (req, res, next) {
    getData(`${API_URL}/getAdminValueSportsPublished`)
        .then(output => res.render('admin-panel/edit', {
            title_head: 'Admin-Sports',
            data: output,
            route: 'pdRnZRfiUaSx2cAcLdK5/admin-sports-published',
            layout: 'admin.hbs'
        }));
});

/** DELETE published */
router.post('/delete-news-entry-published', function (req, res, next) {
    let route = req.body.routeToRender;
    let deleteData = JSON.stringify({ id: req.body.idToDel });
    request({ url: `${API_URL}/v1/delete_news_published`, method: 'POST', json: deleteData },
        function (error, response) {
            if (!error && response.statusCode == 200) res.redirect(route);
            else res.send(error);
        });
});

/** EDIT published */
router.post('/update-entry-published', function (req, res, next) {
    let route = req.body.routeToRender;
    let newsData = JSON.stringify({
        publisher: req.body.publisher, title: req.body.title,
        description: req.body.description, urlToImage: req.body.urlToImage,
        category: req.body.category, publishedAt: req.body.publishedAt,
        createdAt: req.body.createdAt, hashtags: req.body.hashtags,
        sentiment: req.body.sentiment, url: req.body.url,
        id: req.body.idToEdit, desc_line: req.body.desc_line
    });
    request({ url: `${API_URL}/v1/edit_news_story_published`, method: 'POST', json: newsData },
        function (error, response) {
            if (!error && response.statusCode == 200) res.redirect(route);
            else res.send(error);
        });
});

/** ADD news */
router.post('/add-entry', function (req, res, next) {
    let route = req.body.routeToRender;
    let newsData = JSON.stringify({
        publisher: req.body.publisher, urlToImage: req.body.urlToImage,
        url: req.body.url, title: req.body.title,
        description: req.body.description, hashtags: req.body.hashtags,
        category: req.body.category,
    });
    request({ url: `${API_URL}/v1/addnews`, method: 'POST', json: newsData },
        function (error, response) {
            if (!error && response.statusCode == 200) res.redirect(route);
            else res.send(error);
        });
});

/** Get summary from URL */
router.post('/get-link-data', function (req, res, next) {
    let route = req.body.routeToRender;
    let newsData = JSON.stringify({ url: req.body.url });
    request({ url: `${API_URL}/v1/getsummaryfromurl`, method: 'POST', json: newsData },
        function (error, response) {
            if (!error && response.statusCode == 200) {
                res.render('admin-panel/addnews-final', {
                    data: response.body, route: route,
                    description: response.body.description,
                    layout: 'admin.hbs'
                });
            } else res.send(error);
        });
});

/** Unpublished sections */
router.get('/pdRnZRfiUaSx2cAcLdK5/admin-trending', function (req, res, next) {
    getData(`${API_URL}/getAdminValueTrending`)
        .then(output => res.render('admin-panel/edit', {
            title_head: 'Admin - Trending', data: output,
            route: 'pdRnZRfiUaSx2cAcLdK5/admin-trending', layout: 'admin.hbs'
        }));
});

router.get('/pdRnZRfiUaSx2cAcLdK5/admin-technology', function (req, res, next) {
    getData(`${API_URL}/getAdminValueTechnology`)
        .then(output => res.render('admin-panel/edit', {
            title_head: 'Admin-Technology', data: output,
            route: 'pdRnZRfiUaSx2cAcLdK5/admin-technology', layout: 'admin.hbs'
        }));
});

router.get('/pdRnZRfiUaSx2cAcLdK5/admin-business', function (req, res, next) {
    getData(`${API_URL}/getAdminValueBusiness`)
        .then(output => res.render('admin-panel/edit', {
            title_head: 'Admin-Business', data: output,
            route: 'pdRnZRfiUaSx2cAcLdK5/admin-business', layout: 'admin.hbs'
        }));
});

router.get('/pdRnZRfiUaSx2cAcLdK5/admin-entertainment', function (req, res, next) {
    getData(`${API_URL}/getAdminValueEntertainment`)
        .then(output => res.render('admin-panel/edit', {
            title_head: 'Admin-Entertainment', data: output,
            route: 'pdRnZRfiUaSx2cAcLdK5/admin-entertainment', layout: 'admin.hbs'
        }));
});

router.get('/pdRnZRfiUaSx2cAcLdK5/admin-health', function (req, res, next) {
    getData(`${API_URL}/getAdminValueHealth`)
        .then(output => res.render('admin-panel/edit', {
            title_head: 'Admin-Health', data: output,
            route: 'pdRnZRfiUaSx2cAcLdK5/admin-health', layout: 'admin.hbs'
        }));
});

router.get('/pdRnZRfiUaSx2cAcLdK5/admin-sports', function (req, res, next) {
    getData(`${API_URL}/getAdminValueSports`)
        .then(output => res.render('admin-panel/edit', {
            title_head: 'Admin-Sports', data: output,
            route: 'pdRnZRfiUaSx2cAcLdK5/admin-sports', layout: 'admin.hbs'
        }));
});

/** DELETE unpublished */
router.post('/delete-news-entry', function (req, res, next) {
    let route = req.body.routeToRender;
    let deleteData = JSON.stringify({ id: req.body.idToDel });
    request({ url: `${API_URL}/v1/delete_news`, method: 'POST', json: deleteData },
        function (error, response) {
            if (!error && response.statusCode == 200) res.redirect(route);
            else res.send(error);
        });
});

router.post('/edit-news-entry', function (req, res, next) {
    let id = req.body.idToEdit;
    let route = req.body.routeToRender;
    res.redirect('/update' + route + '/' + id);
});

router.get('/update/:route/:id', function (req, res, next) {
    let idToEdit = req.params.id;
    let routeToRender = req.params.route;
    getData(`${API_URL}/description?id=${idToEdit}`)
        .then(output => res.render('admin-panel/edit', {
            data: output, route: routeToRender, layout: 'admin.hbs'
        }));
});

router.post('/update-entry', function (req, res, next) {
    let route = req.body.routeToRender;
    let newsData = JSON.stringify({
        publisher: req.body.publisher, title: req.body.title,
        description: req.body.description, urlToImage: req.body.urlToImage,
        category: req.body.category, publishedAt: req.body.publishedAt,
        createdAt: req.body.createdAt, hashtags: req.body.hashtags,
        sentiment: req.body.sentiment, url: req.body.url,
        id: req.body.idToEdit, desc_line: req.body.desc_line
    });
    request({ url: `${API_URL}/v1/edit_news_story`, method: 'POST', json: newsData },
        function (error, response) {
            if (!error && response.statusCode == 200) res.redirect(route);
            else res.send(error);
        });
});

router.get('/', function (req, res, next) {
    res.redirect('login');
});

module.exports = router;
