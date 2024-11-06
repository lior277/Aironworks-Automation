import http from 'k6/http';
import exec from 'k6/execution';
// import { open } from 'k6/experimental/fs';
import papaparse from 'https://jslib.k6.io/papaparse/5.1.1/index.js';
import { SharedArray } from 'k6/data';
import { check, sleep } from 'k6';

const BASE_URL = 'https://staging.app.aironworks.com';
const data = new SharedArray('cases', function () {
  // here you can open files, and then do additional processing or generate the array with data dynamically
  const f = JSON.parse(open('perf_warning_page.json'));
  return f; // f must be an array[]
});

export let options = {
  scenarios: {
    warning_page: {
      executor: 'per-vu-iterations',
      vus: 100,
      iterations: 30,
      maxDuration: '30s',
    }
  }
};

export default function(){
    let tags = { testid: 'warning_page' };
    //Get data from data set
    let currentIndex = exec.scenario.iterationInTest % data.length;
    console.log("Current Index:"+currentIndex);
    let row = data[currentIndex];
    console.log("Data:"+typeof(row));
    let url = row.attack_url;

    let payload = JSON.stringify({'url': url });
    let params = {
      headers: {
        'Content-Type': 'application/json',
      },
      tags: tags
    };
    let res = http.post(BASE_URL + '/api/public/verify_url_click', payload, params);

    console.log("Response code:"+res.status);
    console.log("Response:"+res.body);

    //Check if response is not 200
    check(res, {
        'is status 200': (r) => r.status === 200,
    });
}
