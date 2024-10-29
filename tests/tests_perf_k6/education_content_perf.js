import http from 'k6/http';
// import { open } from 'k6/experimental/fs';
import papaparse from 'https://jslib.k6.io/papaparse/5.1.1/index.js';
import { SharedArray } from 'k6/data';
import { check, sleep } from 'k6';

const BASE_URL = 'https://staging.app.aironworks.com';
const data = new SharedArray('users', function () {
  // here you can open files, and then do additional processing or generate the array with data dynamically
  const f = JSON.parse(open('./perf_education_campaign.json'));
  return f; // f must be an array[]
});

export let options = {
    vus: 10,
    duration: '20s',
    iterations: 100,
};

export default function(){
    let tags = { testid: 'k8s' };
    //Get data from data set
    let currentIndex = __ITER % data.length;
    let row = data[currentIndex];
    console.log("Data:"+typeof(row));
    let assignmentId = row.id;
    //let url = BASE_URL + '/api/education/assignment/'+ assignmentId;
    let url = BASE_URL + '/api/education/assignment/'+ assignmentId + '?email=' + row.email + '&token=' + row.token;
    let res = http.get(url, {tags: tags});
    //Check if response is not 200
    check(res, {
        'is status 200': (r) => r.status === 200,
    });
}



