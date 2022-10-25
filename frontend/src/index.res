// Hot Module Replacement (HMR) - Remove this snippet to remove HMR.
// Learn more: https://www.snowpack.dev/#hot-module-replacement
@scope(("import", "meta")) @val external hot: bool = "hot"

@scope(("import", "meta", "hot")) @val
external accept: unit => unit = "accept"

%%raw(`import './index.css';`)

let headers = () =>
  Axios.Headers.fromObj({
    "Content-Type": "application/json",
});
let config = Axios.makeConfig(
  ~headers=headers(),
  ~timeout=5000,
  ()
)

let fetchData = () => { 
    Axios.get("http://localhost:8081/stock-name?name=데브시스터즈", ~config, ()) 
  ->Promise.Js.toResult 
  ->Promise.mapOk(({data}) => Js.log(data))
  ->Promise.tapError(err => {
    switch (err.response) {
      | Some({status: 404}) => Js.log("Not found")
      | e => Js.log2("an error occured", e)
    } 
  })
  ->ignore
}

if true{
  fetchData()
}
ReactDOM.render(
  <React.StrictMode> <App /> </React.StrictMode>,
  ReactDOM.querySelector("#root")->Belt.Option.getExn,
)

if hot {
  accept()
}
