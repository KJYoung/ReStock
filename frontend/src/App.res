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

let fetchData = () => { 
    Axios.get("http://localhost:8081/stock-name?name=데브시스터즈&pageNo=2", ~config, ()) 
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

@react.component
let make = () => {
  let (count, setCount) = React.useState(() => 0.)

  React.useEffect0(() => {
    let intervalId = Js.Global.setInterval(() => setCount(count => count +. 1.), 100)

    Some(() => Js.Global.clearInterval(intervalId))
  })

  <div className="App">
    <header className="App-header">
      <button onClick={(e) => fetchData()} >{React.string("Fetch")}</button>
      <img src=logo className="App-logo" alt="logo" />
      <p>
        {React.string("Edit ")}
        <code> {React.string("src/App.jsx")} </code>
        {React.string(" and save to reload.")}
      </p>
      <p>
        {React.string("Page has been open for ")}
        <code> {React.string(Js.Float.toFixedWithPrecision(count /. 10., ~digits=1))} </code>
        {React.string(" seconds")}
      </p>
      <a className="App-link" href="https://reactjs.org" target="_blank" rel="noopener noreferrer">
        {React.string("Learn React")}
      </a>
    </header>
  </div>
}
