var express = require('express');
var router = express.Router();
const fetch = require('node-fetch');

const API_URL = process.env.API_URL || 'http://localhost:8080';

// Helper: fetch from main API, fall back to empty on error
async function getData(path) {
    try {
        const res = await fetch(`${API_URL}${path}`);
        if (!res.ok) return null;
        return await res.json();
    } catch (e) {
        console.error(`API fetch error for ${path}:`, e.message);
        return null;
    }
}

function splitNews(newslist) {
    if (!newslist || newslist.length === 0) return [[], [], []];
    let li1 = [], li2 = [], li3 = [];
    const len = newslist.length;
    for (let i = Math.max(0, len - 3); i < len; i++)     li3.push(newslist[i]);
    for (let i = Math.max(0, len - 7); i < len - 3; i++) li2.push(newslist[i]);
    for (let i = 0; i < Math.max(0, len - 7); i++)       li1.push(newslist[i]);
    return [li1, li2, li3];
}

// ── Routes ────────────────────────────────────────────────────────────────────

router.get('/', async function(req, res) {
    try {
        const data = await getData('/homepage');
        if (!data) throw new Error('No data from API');
        res.render('index', {
            toptrending:             data[0] || {},
            latestcards:             data[1] || [],
            trending_news_list:      data[2] || [],
            row1_video:              data[3] || [],
            row2_video:              data[4] || [],
            latestvideo:             data[5] || [],
            topentertainment:        data[6] || {},
            latestEcards:            data[7] || [],
            entertainment_news_list: data[8] || [],
            hash_list:               data[9] || []
        });
    } catch (e) {
        console.error('Homepage error:', e.message);
        res.render('index', { toptrending: {}, latestcards: [], trending_news_list: [], row1_video: [], row2_video: [], latestvideo: [], topentertainment: {}, latestEcards: [], entertainment_news_list: [], hash_list: [] });
    }
});

router.get('/trending', async function(req, res) {
    const data = await getData('/getValueTrending') || [[], []];
    const [li1, li2, li3] = splitNews(data[0] || []);
    res.render('pages/general', { headLine: 'TRENDING', data: li1, latest: li2, suggested: li3, tags: data[1] || [] });
});

router.get('/sports', async function(req, res) {
    const data = await getData('/getValueSports') || [[], []];
    const [li1, li2, li3] = splitNews(data[0] || []);
    res.render('pages/general', { headLine: 'SPORTS', data: li1, latest: li2, suggested: li3, tags: data[1] || [] });
});

router.get('/technology', async function(req, res) {
    const data = await getData('/getValueTechnology') || [[], []];
    const [li1, li2, li3] = splitNews(data[0] || []);
    res.render('pages/general', { headLine: 'TECHNOLOGY', data: li1, latest: li2, suggested: li3, tags: data[1] || [] });
});

router.get('/entertainment', async function(req, res) {
    const data = await getData('/getValueEntertainment') || [[], []];
    const [li1, li2, li3] = splitNews(data[0] || []);
    res.render('pages/general', { headLine: 'ENTERTAINMENT', data: li1, latest: li2, suggested: li3, tags: data[1] || [] });
});

router.get('/business', async function(req, res) {
    const data = await getData('/getValueBusiness') || [[], []];
    const [li1, li2, li3] = splitNews(data[0] || []);
    res.render('pages/general', { headLine: 'BUSINESS', data: li1, latest: li2, suggested: li3, tags: data[1] || [] });
});

router.get('/health', async function(req, res) {
    const data = await getData('/getValueHealth') || [[], []];
    const [li1, li2, li3] = splitNews(data[0] || []);
    res.render('pages/general', { headLine: 'HEALTH', data: li1, latest: li2, suggested: li3, tags: data[1] || [] });
});

router.get('/world', async function(req, res) {
    const data = await getData('/getValueWorld') || [[], []];
    const [li1, li2, li3] = splitNews(data[0] || []);
    res.render('pages/general', { headLine: 'WORLD', data: li1, latest: li2, suggested: li3, tags: data[1] || [] });
});

router.get('/hindi', async function(req, res) {
    const data = await getData('/getValueHindi') || [[], []];
    const [li1, li2, li3] = splitNews(data[0] || []);
    res.render('pages/general', { headLine: 'HINDI', data: li1, latest: li2, suggested: li3, tags: data[1] || [] });
});

router.get('/hashtag/:tagName', async function(req, res) {
    const tag = req.params.tagName;
    const data = await getData(`/v1/showtags?tagName=${tag}`) || [[], []];
    res.render('hashtag_page', { title_head: 'VIEW - ' + tag, data: data[0] || [], tags: data[1] || [] });
});

router.get('/description/:desc/:idname', async function(req, res) {
    const id = req.params.idname;
    const data = await getData(`/description?id=${id}`) || [];
    res.render('pages/description', {
        data: data[0] || {},
        toptrending: (data[1] || []).slice(0, 5),
        cards: (data[1] || []).slice(5),
        tags: data[2] || [],
        layout: 'description.hbs'
    });
});

router.get('/search_hashtag', async function(req, res) {
    const data = await getData('/searchtags') || [];
    res.json(data);
});

module.exports = router;
