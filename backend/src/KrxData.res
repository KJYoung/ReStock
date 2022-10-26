
open Express

@module("dotenv")
external config: unit => unit = "config"
let _ = config();

@scope(("process")) 
external env: TypeInterface.dotenvObj = "env"
let kRX_KEY = env["KRX_DATA_KEY"];

let headers = () =>
  Axios.Headers.fromObj({
      "Host": "apis.data.go.kr", 
      "Content-Type": "application/json",
      "User-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36"
  });

let config = Axios.makeConfig(
  ~headers=headers(),
  ~timeout=5000,
  ()
)

let baseURL = `https://apis.data.go.kr/1160100/service/GetStockSecuritiesInfoService/getStockPriceInfo?serviceKey=${kRX_KEY}&resultType=json`
let getStockPriceInfoTest = (_req, res) => {
  let fetchData = () => {
    Axios.get(baseURL, ~config, ()) 
    ->Promise.Js.toResult 
    ->Promise.mapOk(({data}) => {
      Js.log(data["response"]["body"]["items"])
      res->status(200)->json(data["response"]["body"]["items"])
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
}
let getStockPriceInfoByName = (req, res) => {
  let reqQuery = req->query;
  let fetchData = () => {

    let url = Js.String.concatMany(
      [`&itmsNm=${reqQuery["name"]}`, `&pageNo=${reqQuery["pageNo"]}`],
      baseURL
    )
    Axios.get(url, ~config, ()) 
    ->Promise.Js.toResult 
    ->Promise.mapOk(({data}) => {
      let _ = res->set("Access-Control-Allow-Origin", "http://localhost:8080")
      let _ = res->status(200)->json(data)
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
}