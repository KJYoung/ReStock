open Express

let app = expressCjs()
let router = Router.make()

type dotenvObj = {
  "KRX_OPENAPI_KEY": string,
  "KRX_DATA_KEY": string,
  "NODE_TLS_REJECT_UNAUTHORIZED" : string
}

type axiosResObj = {
  "response" : {
    "header" : {
      "resultCode" : string,
      "resultMsg"  : string
    },
    "body" : {
      "numOfRows"  : int,
      "pageNo"     : int,
      "totalCount" : int,
      "items"      : {
        
      }
    }
  }
}
// Import nodejs' path.dirname
@module("dotenv")
external config: unit => unit = "config"
let _ = config();


@scope(("process")) 
external env: dotenvObj = "env"
let kRX_KEY = env["KRX_DATA_KEY"];

router->Router.use((req, _res, next) => {
  Js.log(req)
  next()
})

router->Router.useWithError((err, _req, res, _next) => {
  Js.Console.error(err)
  let _ = res->status(500)->endWithData("An error occured")
})

app->useRouterWithPath("/someRoute", router)

app->use(jsonMiddleware())

app->get("/", (_req, res) => {
  let _ = res->set("Access-Control-Allow-Origin", "http://localhost:8080")
  let _ = res->status(200)->json({"ok": true})
})

// app->get("/stock/", (_req, res) => {
//   let fetchData = () => {
//     let headers = () =>
//       Axios.Headers.fromObj({"AUTH_KEY": `${kRX_KEY}`, "apiId": "ksq_bydd_trd"});
//     let config = Axios.makeConfig(
//             ~headers=headers(),
//             ()
//         )
//     Axios.get("http://data-dbg.krx.co.kr/svc/apis/sto/ksq_bydd_trd", ~config, ()) 
//     ->Promise.Js.toResult 
//     ->Promise.mapOk(({data}) => res->status(200)->json(data))
//     ->Promise.tapError(err => {
//       switch (err.response) {
//         | Some({status: 404}) => Js.log("Not found")
//         | e => Js.log2("an error occured", e)
//       } 
//     })
//     ->ignore
//   }
//   fetchData();
// })
app->get("/stock2/", (_req, res) => {
  let fetchData = () => {
    let headers = () =>
      Axios.Headers.fromObj({
        "Host": "apis.data.go.kr", 
        "Content-Type": "application/json",
        "User-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36"}
      );
      
    let config = Axios.makeConfig(
            ~headers=headers(),
            ~timeout=5000,
            ()
        )
    let url = `https://apis.data.go.kr/1160100/service/GetStockSecuritiesInfoService/getStockPriceInfo?serviceKey=${kRX_KEY}&resultType=json`
    Js.log(url)
    Axios.get(url, ~config, ()) 
    ->Promise.Js.toResult 
    ->Promise.mapOk(({data}) => {
      Js.log(data["response"]["body"]["items"])
    })
    ->Promise.tapError(err => {
      switch (err.response) {
        | Some({status: 404}) => Js.log("Not found")
        | e => Js.log2("an error occured", e)
      } 
    })
    ->ignore
  }
  fetchData();
  
})
app->post("/ping", (req, res) => {
  let body = req->body
  let _ = switch body["name"]->Js.Nullable.toOption {
  | Some(name) => res->status(200)->json({"message": `Hello ${name}`})
  | None => res->status(400)->json({"error": `Missing name`})
  }
})

app->all("/allRoute", (_req, res) => {
  res->status(200)->json({"ok": true})->ignore
})

app->useWithError((err, _req, res, _next) => {
  Js.Console.error(err)
  let _ = res->status(500)->endWithData("An error occured")
})

let port = 8081
let _ = app->listenWithCallback(port, _ => {
  Js.Console.log(`Listening on http://localhost:${port->Belt.Int.toString}`);
  Js.Console.log(kRX_KEY);
})