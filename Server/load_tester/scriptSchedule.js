import  http  from "k6/http";
import { check, sleep } from "k6";
import { Rate } from "k6/metrics";
export const errorRate = new Rate("errors")

export default function () {
    const url = "http://161.35.253.194/api/v1/courses/1/parallels/1";


    check(http.get(url), {
        'status is accepted': (r) => (r.status >= 200 && r.status < 400),
    }) || errorRate.add(1)

    sleep(0.8)
}
