@module("./logo.svg") external logo: string = "default"

%%raw(`import './App.css';`)

let headers = () =>
  Axios.Headers.fromObj({
    "Content-Type": "application/json",
});
let config = Axios.makeConfig(
  ~headers=headers(),
  ~timeout=5000,
  ()
)

let baseURL = "http://localhost:8000/stockKR/api"


@react.component
let make = () => {
  let (result, setResult) = React.useState(() => "Not Yet")
  // let (count, setCount) = React.useState(() => 0.)

  // React.useEffect0(() => {
  //   // let intervalId = Js.Global.setInterval(() => setCount(count => count +. 1.), 100)
  //   // Some(() => Js.Global.clearInterval(intervalId))
  // })

  let fetchData = () => {
      Axios.get( baseURL ++ "/", ~config, ()) 
    ->Promise.Js.toResult 
    ->Promise.mapOk(({data}) => {
      Js.log(data)
      setResult(data["Hi"])
    })
    ->Promise.tapError(err => {
      switch (err.response) {
        | Some({status: 404}) => Js.log("Not found")
        | e => Js.log2("an error occured", e)
      } 
    })
    ->ignore
  }

  <div className="App">
    <header className="App-header">
      <button onClick={(_e) => fetchData()} >{React.string("Fetch")}</button>
      <button onClick={(_e) => setResult((_s) => "Cleaned") } >{React.string("Clear")}</button>
      <p>{React.string(result)}</p>
    </header>
  </div>
}
