Release Notes
---

## [1.4.5](https://github.com/osl-incubator/satellite-weather-downloader/compare/1.4.4...1.4.5) (2023-01-24)


### Bug Fixes

* **celery:** create different queues to their own tasks ([39e4e40](https://github.com/osl-incubator/satellite-weather-downloader/commit/39e4e409076deec4da005cd7437ec54dddaab7d0))

## [1.4.4](https://github.com/osl-incubator/satellite-weather-downloader/compare/1.4.3...1.4.4) (2023-01-23)


### Bug Fixes

* **downloader:** date column is called time ([#24](https://github.com/osl-incubator/satellite-weather-downloader/issues/24)) ([c1b16ff](https://github.com/osl-incubator/satellite-weather-downloader/commit/c1b16ff8875c85f55d4e861f61d72fc8f41b33b9))
* **readme:** typo ([ea46efc](https://github.com/osl-incubator/satellite-weather-downloader/commit/ea46efce2b8a9d5e21733a9dcbd99c7b2bd22dad))

## [1.4.3](https://github.com/osl-incubator/satellite-weather-downloader/compare/1.4.2...1.4.3) (2023-01-23)


### Bug Fixes

* **conda:** use SWD pypi package ([9014f91](https://github.com/osl-incubator/satellite-weather-downloader/commit/9014f91825ca10a966d99d0687fc847b44630e3a))

## [1.4.2](https://github.com/osl-incubator/satellite-weather-downloader/compare/1.4.1...1.4.2) (2023-01-23)


### Bug Fixes

* **downloader:** minor fix on transforming dates ([#23](https://github.com/osl-incubator/satellite-weather-downloader/issues/23)) ([7f56054](https://github.com/osl-incubator/satellite-weather-downloader/commit/7f56054202e0336d3f7a791baec380c8c2596f92))

## [1.4.1](https://github.com/osl-incubator/satellite-weather-downloader/compare/1.4.0...1.4.1) (2023-01-23)


### Bug Fixes

* **ci:** remove unecessary files to release ([dcb2521](https://github.com/osl-incubator/satellite-weather-downloader/commit/dcb2521230f733b8388c0cb149750f7d0dd31375))
* **ci:** removing leftovers ([16dc9fb](https://github.com/osl-incubator/satellite-weather-downloader/commit/16dc9fbd5de2325da3874b71612073eb89e21bd8))
* **ci:** rollback conda version on ci ([ae02392](https://github.com/osl-incubator/satellite-weather-downloader/commit/ae02392d3bf827276aac81bcb8b83ad898ce33cd))
* **release:** try adding setup-node  ([ffb3be9](https://github.com/osl-incubator/satellite-weather-downloader/commit/ffb3be94bb2b8feb1ea2379b52ebd347c9e1285b))
* **semantic-release:** pin node version on npx ([#16](https://github.com/osl-incubator/satellite-weather-downloader/issues/16)) ([e30b7e5](https://github.com/osl-incubator/satellite-weather-downloader/commit/e30b7e5f68626216991566aad1e7ebe5b7f6f7a6))
* **semantic-release:** pin node version on npx ([#17](https://github.com/osl-incubator/satellite-weather-downloader/issues/17)) ([d13498d](https://github.com/osl-incubator/satellite-weather-downloader/commit/d13498d1188eecdf8b2be943814551265274f182))

# [1.4.0](https://github.com/osl-incubator/satellite-weather-downloader/compare/1.3.0...1.4.0) (2022-11-25)


### Features

* **flower:** Add flower to keep a better track of celery tasks ([#7](https://github.com/osl-incubator/satellite-weather-downloader/issues/7)) ([d551d83](https://github.com/osl-incubator/satellite-weather-downloader/commit/d551d838e4be85ef776b353464b1600d941c7ecc))

# [1.3.0](https://github.com/osl-incubator/satellite-weather-downloader/compare/1.2.0...1.3.0) (2022-11-25)


### Features

* **celery task:** The ability of backfilling copernicus data ([#5](https://github.com/osl-incubator/satellite-weather-downloader/issues/5)) ([80b43c9](https://github.com/osl-incubator/satellite-weather-downloader/commit/80b43c939b18747b6fbf2aa8d893c5209068b05f))

# [1.2.0](https://github.com/osl-incubator/satellite-weather-downloader/compare/1.1.0...1.2.0) (2022-11-23)


### Features

* **copernicus:** Collect weather data from Copernicus API ([#3](https://github.com/osl-incubator/satellite-weather-downloader/issues/3)) ([991d1ec](https://github.com/osl-incubator/satellite-weather-downloader/commit/991d1ec7025e2a97555ad54b03589d3d02711e38))

# [1.1.0](https://github.com/osl-incubator/satellite-weather-downloader/compare/1.0.0...1.1.0) (2022-09-23)


### Bug Fixes

* **CI:** Update service name to start container ([87678fd](https://github.com/osl-incubator/satellite-weather-downloader/commit/87678fd06b1ddf6a921bdf8a3ce37fe7ef1c7357))


### Features

* **app:** Add satellite_weather_downloader ([8d3ecc0](https://github.com/osl-incubator/satellite-weather-downloader/commit/8d3ecc00ef37eb49060c7c586f6489214aab17d9))
* **app:** Remove the downloader_app directory ([8813096](https://github.com/osl-incubator/satellite-weather-downloader/commit/88130967e289850f4f228ca20cdadcf64277a756))
* **build:** Update build dependencies ([6b5b559](https://github.com/osl-incubator/satellite-weather-downloader/commit/6b5b55918578cf284019fc6f11d7e073f1a84501))