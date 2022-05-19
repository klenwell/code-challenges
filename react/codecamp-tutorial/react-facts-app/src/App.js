import React from 'react'
import './App.css';
import Navbar from './components/Navbar'
import Main from './components/Main'
import CsvTable from './components/CsvTable'


const SHEET_ID = '1M7BfyPuwHQiavFtH59sgI9lJ7HjBpjXdBB-5BWv15K4'
const CSV_URL = `https://docs.google.com/spreadsheets/d/${SHEET_ID}/gviz/tq?tqx=out:csv&sheet=Data`


function onFetchComplete(results, setStateFn) {
	console.log("results:", results)

  const covidData = results.data.filter(row => {
    const hasDate = !!row.Date
    const hasTestPosRate = !!row['Test Pos Rate 7d Avg']
    return hasDate && hasTestPosRate
  })

  setStateFn(covidData)
  console.log("covidData:",  covidData)
}

function onFetchError(err, file) {
	console.error("ERROR:", err, file);
}


function App() {
  let Papa = window.Papa

  const [ocCovidData, setOcCovidData] = React.useState([])

  function fetchCovidData() {
    const papaConfig = {
  		header: true,
  		dynamicTyping: true,
  		skipEmptyLines: true,
  		complete: function(results) { onFetchComplete(results, setOcCovidData) },
  		error: onFetchError,
  		download: true
  	}

    console.log('Fetching data...')
    Papa.parse(CSV_URL, papaConfig)
  }

  React.useEffect(() => {
    console.log('useEffect')
    fetchCovidData()
  }, [])

  return (
    <div className="container">
      <Navbar />
      <Main />
      {ocCovidData.length > 0 && <CsvTable data={ocCovidData} />}
    </div>
  )
}

export default App;
