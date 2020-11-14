import fetch from "../util/fetch-fill";
import URI from "urijs";

// /records endpoint
window.path = "http://localhost:3000/records";

// Constants
const primaryColors = ['red', 'blue', 'yellow'];

// Your retrieve function plus any additional functions go here ...
function retrieve(options = {}) {
  // Options
  let page = options.page || 1;
  let colors = options.colors || [];

  // Build URI.
  let limit = 10;
  let offset = (page - 1) * limit;
  let uri = URI(window.path);
  uri.search({ limit: limit, offset: offset });

  if (colors.length > 0) {
    colors.forEach(color => uri.addSearch('color[]', color));
  }
  console.log(uri.toString())

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
    payload.previousPage = page == 1 ? null : page - 1;
    payload.nextPage = page + 1;
    console.log(payload);
    return payload;
  })
  .catch((error) => {
    console.log('Error:', error);
    return null;
  });
}

// Helper methods
function isPrimaryClosed(record) {
  return record.disposition == 'closed' && primaryColors.includes(record.color);
}

export default retrieve;
