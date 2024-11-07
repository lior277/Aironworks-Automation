import http from 'k6/http';
import exec from 'k6/execution';
import { SharedArray } from 'k6/data';
import { check } from 'k6';

const BASE_URL = 'https://staging.app.aironworks.com';
const data = new SharedArray('cases', function () {
  // here you can open files, and then do additional processing or generate the array with data dynamically
  const f = JSON.parse(open('data.json'));
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
    let currentIndex = exec.scenario.iterationInTest % data.length;
    let row = data[currentIndex];
    console.log("Data:"+typeof(row));
    let url = row.attack_url;

    let payload = JSON.stringify({'url': url });
    let params = {
    headers: {
      'Content-Type': 'application/json',
    },
    };
    let res = http.get(BASE_URL + '/warning_page', payload, params, {tags: tags});
    //Check if response is not 200
    check(res, {
        'is status 200': (r) => r.status === 200,
    });

}
