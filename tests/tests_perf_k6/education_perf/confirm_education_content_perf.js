import http from 'k6/http';
import exec from 'k6/execution';
import { SharedArray } from 'k6/data';
import { check } from 'k6';

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
    let currentIndex = exec.scenario.iterationInTest % data.length;
    let row = data[currentIndex];
    console.log("Data:"+typeof(row));
    let assignmentId = row.id;
    let url = BASE_URL + '/api/education/assignment/'+ assignmentId + '?email=' + row.email + '&token=' + row.token;
    let res = http.get(url, {tags: tags});
    //Check if response is not 200
    check(res, {
        'is status 200': (r) => r.status === 200,
    });
    let url2 = BASE_URL + '/api/education/assignment/'+ assignmentId +'/submit';
    let payload = JSON.stringify({'email': row.email, 'token': row.token});
    let params = {
      headers: {
        'Content-Type': 'application/json',
      },
      tags: tags,
    };
    let res2 = http.post(url2, payload, params, {tags: tags});
    //Check if response is not 200
    check(res2, {
        'is status 200': (r) => r.status === 200,
    });
}



