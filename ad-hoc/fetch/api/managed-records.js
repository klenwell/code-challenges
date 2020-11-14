import fetch from "../util/fetch-fill";
import URI from "urijs";

// /records endpoint
window.path = "http://localhost:3000/records";

// Constants
const primaryColors = ['red', 'blue', 'yellow'];

// Your retrieve function plus any additional functions go here ...
function retrieve(options) {
  let uri = URI(window.path)

  uri.search({ page: 1, colors: [] });

  // Docs: https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API/Using_Fetch
  return fetch(uri)
  .then(response => {
    console.log(response.status);
    return response.json()
  })
  .then(records => {
    records = records.slice(0, 10);
    console.log(records.length, records[0]);
    let payload = {};
    payload.ids = records.map(record => record.id);
    payload.open = records.filter(record => record.disposition == 'open');
    payload.open.forEach(record => record.isPrimary = primaryColors.includes(record.color));
    payload.closedPrimaryCount = records.filter(record => isPrimaryClosed(record)).length;
    payload.previousPage = null;
    payload.nextPage = 2;
    console.log(payload);
    return payload;
  })
  .catch((error) => {
    console.error('Error:', error);
  });
}

// Helper methods
function isPrimaryClosed(record) {
  return record.disposition == 'closed' && primaryColors.includes(record.color);
}

export default retrieve;
