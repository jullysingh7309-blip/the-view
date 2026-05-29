let express = require('express');
let createError = require('http-errors');
let router = express.Router();
const fetch = require("node-fetch");

const SUPABASE_URL = process.env.SUPABASE_URL || '';
const SUPABASE_SERVICE_KEY = process.env.SUPABASE_SERVICE_KEY || '';

router.get("/login", function (req, res) {
    res.render('admin-panel/login', {
        layout: 'login.hbs',
        SUPABASE_URL: SUPABASE_URL,
        SUPABASE_ANON_KEY: 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImNwZW1zd2h6cnV4bWpoc3N2ZHRoIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODAwNTA1NjgsImV4cCI6MjA5NTYyNjU2OH0.Fb2M_4aWL669frlkrb63Ug_o7EqWHnA3pNbvGt8pNXI'
    })
});

router.post("/sessionLogin", async (req, res) => {
    const accessToken = req.body.idToken ? req.body.idToken.toString() : '';

    const resp = await fetch(`${SUPABASE_URL}/auth/v1/user`, {
        headers: {
            'Authorization': `Bearer ${accessToken}`,
            'apikey': SUPABASE_SERVICE_KEY
        }
    });
    if (resp.status !== 200) {
        console.log("Auth error:", await resp.text())
        return res.status(401).send("UNAUTHORIZED REQUEST!");
    }
    const user = await resp.json();

    const expiresIn = 60 * 60 * 24 * 5 * 1000;
    console.log("Create Session")
    const options = { maxAge: expiresIn, httpOnly: true, sameSite: 'lax' };
    res.cookie("session", accessToken, options);
    res.end(JSON.stringify({ status: "success" }));
});


router.get("/sessionLogout", (req, res) => {
    res.clearCookie("session");
    res.redirect("/login");
});


module.exports = router;
