// Generated by ReScript, PLEASE EDIT WITH CARE
'use strict';

var Curry = require("rescript/lib/js/curry.js");
var Dotenv = require("dotenv");
var Express = require("express");

var app = Express();

var router = Express.Router();

router.use(function (req, _res, next) {
      console.log(req);
      Curry._1(next, undefined);
    });

router.use(function (err, _req, res, _next) {
      console.error(err);
      res.status(500).end("An error occured");
    });

app.use("/someRoute", router);

app.use(Express.json());

app.get("/", (function (_req, res) {
        res.set("Access-Control-Allow-Origin", "http://localhost:8080");
        res.status(200).json({
              ok: true
            });
      }));

app.post("/ping", (function (req, res) {
        var body = req.body;
        var name = body.name;
        if (name == null) {
          res.status(400).json({
                error: "Missing name"
              });
        } else {
          res.status(200).json({
                message: "Hello " + name + ""
              });
        }
      }));

app.all("/allRoute", (function (_req, res) {
        res.status(200).json({
              ok: true
            });
      }));

app.use(function (err, _req, res, _next) {
      console.error(err);
      res.status(500).end("An error occured");
    });

Dotenv.config();

var openapi = process.env.KRX_OPENAPI_KEY;

app.listen(8081, (function (param) {
        console.log("Listening on http://localhost:" + String(8081) + "");
        console.log(openapi);
      }));

var port = 8081;

exports.app = app;
exports.router = router;
exports.openapi = openapi;
exports.port = port;
/* app Not a pure module */
