
import http from 'k6/http';
import { check } from 'k6';

export const options = {
  stages: [
    { target: 50, duration: '30s' },
    { target: 0, duration: '10' }
  ],
};

export default function () {
  let tags = { testid: 'k8s' };
  const result = http.get('https://test-api.k6.io/public/crocodiles/',{tags: tags});
  check(result, {
    'http response status code is 200': result.status === 200,
  });
}
