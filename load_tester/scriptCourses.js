import  http  from "k6/http";
import { check, sleep } from "k6";
import { Rate } from "k6/metrics";
export const errorRate = new Rate("errors")

export default function () {
    const url = "http://174.138.110.82/api/v1/courses";
    const params = {
        timeout: "90s"
    }

    check(http.get(url), {
        'status is 200': (r) => r.status == 200,
    }) || errorRate.add(1)

    sleep(1)
}
