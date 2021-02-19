# GPSClustering

Given project is created to solve clustering problem for GPS records

## 1. **Data**

Before running project, you need to dowload data by execton next command:

```bash
source prepare_data.sh
```

## 2. **Architecture** of pipeline #1 (Detection of potential waste collection)

![Architecture](docs/Diagrams/Pipeline_1_filtering_problem.png)

## 3. **Managmenet options**

Do next commands from project directory:

* to start contianer: `source start.sh` (creates `/data` folder & runs `docker-compose-dev.yaml`);
* to stop & remove contianer: `source stop.sh`.

## 3. **Environment**

Project has own containerized environment to provide system independence & isolatency.

There are 2 mounting directories:

* `./data`: Directory where data need to be stored. (Mounted as `/Data` within container)
* `./Notebooks`: Directory where data need to be stored. (Mounted as `/Notebooks` within container).

**NOTE**: Everything you do within folders above automatically will be reflected on your host.

## 4. **Other documentations**

* [Dev & Arhitectural recommendations](https://github.com/WasteLabs/GPSClustering/tree/main/docs/Architecture.md)