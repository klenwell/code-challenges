import fetch from "../util/fetch-fill";
import URI from "urijs";

// /records endpoint
window.path = "http://localhost:3000/records";

// Your retrieve function plus any additional functions go here ...
function retrieve(options) {
  uri = URI(window.path)

  // Docs: https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API/Using_Fetch
  return fetch(uri)
  .then(response => {
    console.log(response.status);
    return response.json()
  })
  .then(data => {
    console.log(data.length, data[0]);
    record = {};
    return record;
  })
  .catch((error) => {
    console.error('Error:', error);
  });
}

export default retrieve;
