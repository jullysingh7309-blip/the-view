var express = require('express');
var router = express.Router();

// ── Static mock data using local demo images ─────────────────────────────────

function mockNews(category, images) {
    return images.map((img, i) => ({
        id: category + '_' + i,
        title: category.charAt(0).toUpperCase() + category.slice(1) + ' Story ' + (i + 1),
        description: 'This is a demo description for a ' + category + ' news article. Connect Firebase to load real content.',
        urlToImage: img,
        publisher: 'The View',
        publishedAt: 'May 29, 2026 10:' + String(i).padStart(2,'0') + ' AM',
        createdAt: '2026-05-29',
        category: category,
        desc_line: category + '-story-' + (i + 1),
        hashtags: [category, 'news', 'theview'],
        sentiment: 'Neutral',
        url: '#',
        keyplayers: []
    }));
}

const BASE = '/images/';

const trendingNews   = mockNews('trending',      [BASE+'dashboard/home_1.jpg', BASE+'dashboard/home_2.jpg', BASE+'dashboard/home_3.jpg', BASE+'dashboard/home_7.jpg', BASE+'dashboard/home_8.jpg', BASE+'dashboard/home_9.jpg', BASE+'dashboard/home_10.jpg', BASE+'dashboard/home_11.jpg', BASE+'dashboard/home_12.jpg', BASE+'dashboard/home_13.jpg']);
const entertainNews  = mockNews('entertainment', [BASE+'dashboard/home_7.jpg', BASE+'dashboard/home_8.jpg', BASE+'dashboard/home_9.jpg', BASE+'dashboard/home_14.jpg', BASE+'dashboard/home_15.jpg', BASE+'dashboard/home_16.jpg', BASE+'dashboard/home_17.jpg']);
const sportsNews     = mockNews('sports',        [BASE+'dashboard/home_8.jpg', BASE+'dashboard/home_9.jpg', BASE+'dashboard/home_10.jpg', BASE+'dashboard/home_11.jpg', BASE+'dashboard/home_12.jpg', BASE+'dashboard/home_13.jpg', BASE+'dashboard/home_14.jpg', BASE+'dashboard/home_15.jpg', BASE+'dashboard/home_16.jpg', BASE+'dashboard/home_17.jpg']);
const businessNews   = mockNews('business',      [BASE+'business/business_10.png', BASE+'business/business_11.png', BASE+'business/business_12.png', BASE+'dashboard/home_18.jpg', BASE+'dashboard/home_19.jpg', BASE+'dashboard/home_20.jpg', BASE+'dashboard/home_21.jpg', BASE+'dashboard/home_22.jpg', BASE+'dashboard/home_1.jpg', BASE+'dashboard/home_2.jpg']);
const techNews       = mockNews('technology',    [BASE+'dashboard/home_11.jpg', BASE+'dashboard/home_12.jpg', BASE+'dashboard/home_13.jpg', BASE+'dashboard/home_14.jpg', BASE+'dashboard/home_15.jpg', BASE+'dashboard/home_16.jpg', BASE+'dashboard/home_17.jpg', BASE+'dashboard/home_18.jpg', BASE+'dashboard/home_19.jpg', BASE+'dashboard/home_20.jpg']);
const healthNews     = mockNews('health',        [BASE+'dashboard/home_5.jpg', BASE+'dashboard/home_6.jpg', BASE+'dashboard/home_7.jpg', BASE+'dashboard/home_8.jpg', BASE+'dashboard/home_9.jpg', BASE+'dashboard/home_10.jpg', BASE+'dashboard/home_11.jpg', BASE+'dashboard/home_12.jpg', BASE+'dashboard/home_13.jpg', BASE+'dashboard/home_14.jpg']);
const worldNews      = mockNews('world',         [BASE+'politics/Politics_4.jpg', BASE+'politics/Politics_5.jpg', BASE+'politics/Politics_6.jpg', BASE+'politics/Politics_7.jpg', BASE+'politics/Politics_8.jpg', BASE+'politics/Politics_9.jpg', BASE+'politics/Politics_10.jpg', BASE+'politics/Politics_11.jpg', BASE+'politics/Politics_12.jpg', BASE+'politics/Politics_1.jpg']);
const hindiNews      = mockNews('hindi',         [BASE+'dashboard/home_19.jpg', BASE+'dashboard/home_20.jpg', BASE+'dashboard/home_21.jpg', BASE+'dashboard/home_22.jpg', BASE+'dashboard/home_1.jpg', BASE+'dashboard/home_2.jpg', BASE+'dashboard/home_3.jpg', BASE+'dashboard/home_4.jpg', BASE+'dashboard/home_5.jpg', BASE+'dashboard/home_6.jpg']);

const mockVideos = [0,1,2,3,4,5,6,7,8].map(i => ({
    id: 'video_' + i,
    title: 'Demo Video ' + (i + 1),
    description: 'Video description ' + (i + 1),
    thumbnailUrl: BASE + 'dashboard/home_' + (i + 4) + '.jpg',
    contentUrl: 'https://www.youtube.com/embed/dQw4w9WgXcQ',
    publisher: 'The View',
    publishedAt: 'May 29, 2026',
    createdAt: '2026-05-29',
    url: '#'
}));

const mockTags = ['trending','politics','sports','technology','business','entertainment','health','world','india','economy'].map(t => ({ tagName: t }));
const mockKeyPlayers = [
    { keyplayer: 'John Doe',    img: BASE + 'faces/face1.jpg' },
    { keyplayer: 'Jane Smith',  img: BASE + 'faces/face2.jpg' },
    { keyplayer: 'Alex Johnson',img: BASE + 'faces/face3.jpg' },
    { keyplayer: 'Emily Davis', img: BASE + 'faces/face4.jpg' },
    { keyplayer: 'Chris Lee',   img: BASE + 'faces/face5.jpg' }
];

function splitNews(newslist) {
    let li1 = [], li2 = [], li3 = [];
    const len = newslist.length;
    for (let i = len - 3; i < len; i++)     li3[i - len + 3] = newslist[i];
    for (let i = len - 7; i < len - 3; i++) li2[i - len + 7] = newslist[i];
    for (let i = 0; i < len - 7; i++)       li1[i] = newslist[i];
    return [li1, li2, li3];
}

// ── Routes ────────────────────────────────────────────────────────────────────

router.get('/', function(req, res) {
    res.render('index', {
        toptrending:          trendingNews[0],
        latestcards:          trendingNews.slice(1, 4),
        trending_news_list:   trendingNews.slice(4, 7),
        row1_video:           mockVideos.slice(0, 2),
        row2_video:           mockVideos.slice(2, 4),
        latestvideo:          mockVideos.slice(4, 9),
        topentertainment:     entertainNews[0],
        latestEcards:         entertainNews.slice(1, 5),
        entertainment_news_list: entertainNews.slice(5, 7),
        hash_list:            mockKeyPlayers
    });
});

router.get('/trending', function(req, res) {
    let [li1, li2, li3] = splitNews(trendingNews);
    res.render('pages/general', { headLine: 'TRENDING', data: li1, latest: li2, suggested: li3, tags: mockTags });
});

router.get('/sports', function(req, res) {
    let [li1, li2, li3] = splitNews(sportsNews);
    res.render('pages/general', { headLine: 'SPORTS', data: li1, latest: li2, suggested: li3, tags: mockTags });
});

router.get('/technology', function(req, res) {
    let [li1, li2, li3] = splitNews(techNews);
    res.render('pages/general', { headLine: 'TECHNOLOGY', data: li1, latest: li2, suggested: li3, tags: mockTags });
});

router.get('/entertainment', function(req, res) {
    let [li1, li2, li3] = splitNews(entertainNews);
    res.render('pages/general', { headLine: 'ENTERTAINMENT', data: li1, latest: li2, suggested: li3, tags: mockTags });
});

router.get('/business', function(req, res) {
    let [li1, li2, li3] = splitNews(businessNews);
    res.render('pages/general', { headLine: 'BUSINESS', data: li1, latest: li2, suggested: li3, tags: mockTags });
});

router.get('/health', function(req, res) {
    let [li1, li2, li3] = splitNews(healthNews);
    res.render('pages/general', { headLine: 'HEALTH', data: li1, latest: li2, suggested: li3, tags: mockTags });
});

router.get('/world', function(req, res) {
    let [li1, li2, li3] = splitNews(worldNews);
    res.render('pages/general', { headLine: 'WORLD', data: li1, latest: li2, suggested: li3, tags: mockTags });
});

router.get('/hindi', function(req, res) {
    let [li1, li2, li3] = splitNews(hindiNews);
    res.render('pages/general', { headLine: 'HINDI', data: li1, latest: li2, suggested: li3, tags: mockTags });
});

router.get('/hashtag/:tagName', function(req, res) {
    res.render('hashtag_page', { title_head: 'VIEW - ' + req.params.tagName, data: trendingNews.slice(0, 8), tags: mockTags });
});

router.get('/description/:desc/:idname', function(req, res) {
    const article = trendingNews[0];
    res.render('pages/description', {
        data: article,
        toptrending: trendingNews.slice(1, 6),
        cards: trendingNews.slice(6, 10),
        layout: 'description.hbs'
    });
});

router.get('/search_hashtag', function(req, res) {
    res.json(mockTags);
});

module.exports = router;
