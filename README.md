# dagster_ads

Dagster code location for Astrophysics Data System (ADS) software-defined assets.

Initialized as a [Dagster](https://dagster.io/) project scaffolded with [`dagster project scaffold`](https://docs.dagster.io/getting-started/create-new-project).

## Getting started

First, install your Dagster code location as a Python package.

```bash
make init
```

Then, start the Dagster UI web server, e.g.

```bash
dagster dev -f dagster_ads/deployment.py
```

Open http://localhost:3000 with your browser to see the project.

You can start writing assets in `dagster_ads/assets.py`. The assets are automatically loaded into the Dagster code location as you define them.

## Development


### Adding new Python dependencies

You can specify new Python dependencies in `requirements.in` and `requirements.dev.in`.

Then `make update`.

### Unit testing

Tests are in the `dagster_ads_tests` directory and you can run tests using `pytest`:

```bash
pytest dagster_ads_tests
```

### Schedules and sensors

If you want to enable Dagster [Schedules](https://docs.dagster.io/concepts/partitions-schedules-sensors/schedules) or [Sensors](https://docs.dagster.io/concepts/partitions-schedules-sensors/sensors) for your jobs, the [Dagster Daemon](https://docs.dagster.io/deployment/dagster-daemon) process must be running. This is done automatically when you run `dagster dev`.

Once your Dagster Daemon is running, you can start turning on schedules and sensors for your jobs.