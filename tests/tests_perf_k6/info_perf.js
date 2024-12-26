import http from 'k6/http';
import exec from 'k6/execution';
import { SharedArray } from 'k6/data';
import { check } from 'k6';

const BASE_URL = 'https://staging.app.aironworks.com';


export let options = {
    vus: 10,
    duration: '20s',
    iterations: 100,
};

export default function(){
    let tags = { testid: 'education_content_perf' };
    //Get data from data set
    let url = BASE_URL + '/api/auth/info';
    let res = http.get(url, {tags: tags});
    //Check if response is not 200
    check(res, {
        'is status 200': (r) => r.status === 200,
    });
}



