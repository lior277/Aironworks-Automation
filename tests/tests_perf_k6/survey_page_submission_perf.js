import http from 'k6/http';
// import { open } from 'k6/experimental/fs';
import papaparse from 'https://jslib.k6.io/papaparse/5.1.1/index.js';
import { SharedArray } from 'k6/data';
import { check, sleep } from 'k6';

const BASE_URL = 'https://staging.app.aironworks.com';
const data = new SharedArray('cases', function () {
  // here you can open files, and then do additional processing or generate the array with data dynamically
  const f = JSON.parse(open('../resources/perf_warning_page.json'));
  return f; // f must be an array[]
});

export let options = {
    vus: 10,
    duration: '20s',
    iterations: 100,
};

export default function(){
    //Get data from data set
    let currentIndex = __ITER % data.length;
    let row = data[currentIndex];
    console.log("Data:"+typeof(row));
    let url = row.attack_url;

    let payload = {'url': url };
    let res = http.get(BASE_URL + '/warning_page', payload);
    //Check if response is not 200
    check(res, {
        'is status 200': (r) => r.status === 200,
    });

}