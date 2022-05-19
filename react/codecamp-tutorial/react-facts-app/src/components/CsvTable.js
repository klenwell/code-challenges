import React from 'react'

const WASTEWATER_COL = 'Wastewater 7d (kv / L)'


function wastewaterMetric(rows) {
  const wastewaterRow = rows.find(row => {
    let hasValue = !!row[WASTEWATER_COL]
    return hasValue
  })
  return wastewaterRow
}


export default function CsvTable(props) {
  const data = props.data
  const latest = data[0]
  const wastewater = wastewaterMetric(data)

  console.log('latest:', latest)
  console.log('wastewater:', wastewater)

  return (
    <div className="csv-table">
      <table>
        <caption>Orange County COVID-19 Metrics (as of {latest['Date']})</caption>
        <thead>
          <tr>
            <th>Metric</th>
            <th>Latest</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>Test Positive Rate</td>
            <td>{latest['Test Pos Rate 7d Avg']}</td>
          </tr>
          <tr>
            <td>Daily Cases</td>
            <td>{latest['Cases 7d Avg']}</td>
          </tr>
          <tr>
            <td>
              Wastewater Concentration
              <br />
              <small>(as of {wastewater['Date']})</small>
            </td>
            <td>{wastewater[WASTEWATER_COL]}</td>
          </tr>
        </tbody>
      </table>
    </div>
  )
}
