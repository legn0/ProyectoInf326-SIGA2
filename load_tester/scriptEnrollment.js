import  http  from "k6/http";
import { check, sleep } from "k6";
import { Rate } from "k6/metrics";
export const errorRate = new Rate("errors")

export default function () {
    const url = "http://24.199.67.77/api/v1/courses/1/parallels/2/";


    check(http.get(url), {
        'status is accepted': (r) => (r.status >= 200 && r.status < 400),
    }) || errorRate.add(1)

    sleep(0.8)
}
