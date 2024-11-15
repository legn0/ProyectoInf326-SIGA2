FROM grafana/k6:master-with-browser

WORKDIR /

COPY scriptCourses.js .

CMD ["run", "scriptCourses.js", "--vus", "20", "--duration", "90s"]