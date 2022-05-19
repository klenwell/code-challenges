import React from 'react'
import './App.css';
import Navbar from './components/Navbar'
import Main from './components/Main'
import CsvTable from './components/CsvTable'


const SHEET_ID = '1M7BfyPuwHQiavFtH59sgI9lJ7HjBpjXdBB-5BWv15K4'
const API_URL = `https://docs.google.com/spreadsheets/d/${SHEET_ID}/gviz/tq?tqx=out:csv&sheet=Data`


function App() {

  const [ocCovidData, setocCovidData] = React.useState({})

  function fetchCovidData() {
    setocCovidData([])
  }

  React.useEffect(() => {
  }, [])

  return (
    <div className="container">
      <Navbar />
      <Main />
      <CsvTable />
    </div>
  )
}

export default App;
