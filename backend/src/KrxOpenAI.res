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