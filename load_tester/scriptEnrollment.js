import  http  from "k6/http";
import { check, sleep } from "k6";
import { Rate } from "k6/metrics";
export const errorRate = new Rate("errors")

export default function () {
    const url = "http://24.199.67.77/api/v1/courses";


    check(http.get(url), {
        'status is 200': (r) => r.status == 200,
    }) || errorRate.add(1)

    sleep(0.8)
}
