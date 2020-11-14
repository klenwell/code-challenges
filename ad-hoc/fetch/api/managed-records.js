import fetch from "../util/fetch-fill";
import URI from "urijs";

// /records endpoint
window.path = "http://localhost:3000/records";

// Constants
const primaryColors = ['red', 'blue', 'yellow'];
const pageLimit = 10;

// Your retrieve function plus any additional functions go here ...
function retrieve(options = {}) {
  // Options
  let page = options.page || 1;
  let colors = options.colors || [];

  // Build URI
  let uri = buildUri(page, colors);

  // Docs: https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API/Using_Fetch
  return fetch(uri)
  .then(response => { return response.json() })
  .then(records => { return recordsToPayload(records, page) })
  .catch((error) => {
    console.log('Error:', error);
    return null;
  });
}

// Helper methods
function buildUri(page, colors) {
  let limit = pageLimit + 1; // Include 1 extra record to test if we're on our page.
  let offset = (page - 1) * pageLimit;
  let uri = URI(window.path);

  // Docs: https://medialize.github.io/URI.js/
  uri.search({ limit: limit, offset: offset });
  colors.forEach(color => uri.addSearch('color[]', color));

  return uri;
}

function recordsToPayload(records, page) {
  // What happens if total records are a multiple of 10? This could fail.
  let isLastPage = records.length <= pageLimit;

  // Grab a page full of records.
  records = records.slice(0, 10);

  let payload = {
    ids: records.map(record => record.id),
    open: records.filter(record => record.disposition == 'open'),
    previousPage: page == 1 ? null : page - 1,
    nextPage: isLastPage ? null : page + 1
  };

  // Add isPrimary property to records and count.
  payload.open.forEach(record => record.isPrimary = primaryColors.includes(record.color));
  payload.closedPrimaryCount = records.filter(record => isPrimaryClosed(record)).length;

  return payload;
}

function isPrimaryClosed(record) {
  return record.disposition == 'closed' && primaryColors.includes(record.color);
}

export default retrieve;
