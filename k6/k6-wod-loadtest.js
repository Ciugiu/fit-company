import http from 'k6/http';
import { check, sleep } from 'k6';

export let options = {
  stages: [
    { duration: '30s', target: 10 },
    { duration: '1m', target: 10 },
    { duration: '30s', target: 20 },
    { duration: '1m', target: 20 },
    { duration: '30s', target: 0 },
  ],
};

const BASE_URL = 'http://localhost:5000';
const JWT_TOKEN = 'YOUR_JWT_TOKEN';



export default function () {
  let res = http.get(`${BASE_URL}/fitness/wod`, {
    headers: {
      Authorization: `Bearer ${JWT_TOKEN}`,
    },
  });

  check(res, {
    'status is 200': (r) => r.status === 200,
    'response time < 6000ms': (r) => r.timings.duration < 6000,
  });

  sleep(1);
}