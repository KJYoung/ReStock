open Express

let app = expressCjs()
let router = Router.make()

router->Router.use((req, _res, next) => {
  Js.log(req)
  next()
})

router->Router.useWithError((err, _req, res, _next) => {
  Js.Console.error(err)
  let _ = res->status(500)->endWithData("An error occured!")
})

app->useRouterWithPath("/someRoute", router)

app->use(jsonMiddleware())

app->get("/", (req, res)=> {
  let _ = res->status(200)->json({"meesage": "success2!!"})
})
app->get("/stock/", KrxData.getStockPriceInfoTest)
app->get("/stock-name/", KrxData.getStockPriceInfoByName)
app->post("/ping", (req, res) => {
  let body = req->body
  let _ = switch body["name"]->Js.Nullable.toOption {
  | Some(name) => res->status(200)->json({"message": `Hello ${name}`})
  | None => res->status(400)->json({"error": `Missing name`})
  }
})

app->useWithError((err, _req, res, _next) => {
  Js.Console.error(err)
  let _ = res->status(500)->endWithData("An error occured")
})

let port = 8081
let _ = app->listenWithCallback(port, _ => {
  Js.Console.log(`Listening on http://localhost:${port->Belt.Int.toString}`);
}) 