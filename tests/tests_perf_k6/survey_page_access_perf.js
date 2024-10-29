import http from 'k6/http';
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
    let url = row.attack_url;

    let payload = JSON.stringify({'url': url });
    let params = {
    headers: {
      'Content-Type': 'application/json',
    },
    };
    let res = http.post(BASE_URL + '/api/public/verify_url_click', payload, params, {tags: tags});
    //Check if response is not 200
    check(res, {
        'is status 200': (r) => r.status === 200,
    });
    let survey_id = res.json().id;
    let survey_token = res.json().survey_token;
    let req_url = BASE_URL + '/api/survey/get_surveys_for_attack?attack_id=' + survey_id + '&token=' + survey_token;
    let res2 = http.get(req_url, {tags: tags});
    //Check if response is not 200
    check(res2, {
        'is status 200': (r) => r.status === 200,
    });

}