Release Notes
---

## [1.11.2](https://github.com/AlertaDengue/satellite-weather-downloader/compare/1.11.1...1.11.2) (2025-03-18)


### Bug Fixes

* **dtype:** update epiweek column to integer ([#73](https://github.com/AlertaDengue/satellite-weather-downloader/issues/73)) ([0397a2c](https://github.com/AlertaDengue/satellite-weather-downloader/commit/0397a2c205f99bce9f579da332621c2327577bc3))

## [1.11.1](https://github.com/osl-incubator/satellite-weather-downloader/compare/1.11.0...1.11.1) (2024-11-01)


### Bug Fixes

* **gpkgs:** zip gpkg files to reduce package size (~20%) ([#71](https://github.com/osl-incubator/satellite-weather-downloader/issues/71)) ([f0b668e](https://github.com/osl-incubator/satellite-weather-downloader/commit/f0b668e93b68f04d64c76d8feb2fe44aaaf3430f))

# [1.11.0](https://github.com/osl-incubator/satellite-weather-downloader/compare/1.10.1...1.11.0) (2024-11-01)


### Features

* **copebr:** add locales; include Argenina to weather ([#70](https://github.com/osl-incubator/satellite-weather-downloader/issues/70)) ([b9e2ac1](https://github.com/osl-incubator/satellite-weather-downloader/commit/b9e2ac1d8c06681cd7659acb3fcd2f818f6eafbc))

## [1.10.1](https://github.com/osl-incubator/satellite-weather-downloader/compare/1.10.0...1.10.1) (2024-06-04)


### Bug Fixes

* **epiweek:** fix epiweek value data type ([#68](https://github.com/osl-incubator/satellite-weather-downloader/issues/68)) ([c7cfa18](https://github.com/osl-incubator/satellite-weather-downloader/commit/c7cfa18969339a718a4cc5f9b2e47304688c0433))

# [1.10.0](https://github.com/osl-incubator/satellite-weather-downloader/compare/1.9.6...1.10.0) (2024-06-04)


### Features

* **epiweeks:** include epiweekcolumn on final df ([#67](https://github.com/osl-incubator/satellite-weather-downloader/issues/67)) ([d5c48e2](https://github.com/osl-incubator/satellite-weather-downloader/commit/d5c48e2cf5462900416709cb582787f7b25cd971))

## [1.9.6](https://github.com/osl-incubator/satellite-weather-downloader/compare/1.9.5...1.9.6) (2024-05-16)


### Bug Fixes

* **release:** bump version on PyPI ([#66](https://github.com/osl-incubator/satellite-weather-downloader/issues/66)) ([ce11fb2](https://github.com/osl-incubator/satellite-weather-downloader/commit/ce11fb21315644332fda06756e9de2bcc8d9c859))

## [1.9.5](https://github.com/osl-incubator/satellite-weather-downloader/compare/1.9.4...1.9.5) (2024-05-16)


### Bug Fixes

* **copebr:** round final dataframe to 4 decimals on float values ([#65](https://github.com/osl-incubator/satellite-weather-downloader/issues/65)) ([d8cd3c8](https://github.com/osl-incubator/satellite-weather-downloader/commit/d8cd3c8c6495dff4cb7b7d465a6b7ba42c69c5ee))

## [1.9.4](https://github.com/osl-incubator/satellite-weather-downloader/compare/1.9.3...1.9.4) (2024-03-07)


### Bug Fixes

* **brasil:** update sqlalchemy V1 to V2 due to 'Connection object has no attribute cursor' error ([#64](https://github.com/osl-incubator/satellite-weather-downloader/issues/64)) ([b4b3c13](https://github.com/osl-incubator/satellite-weather-downloader/commit/b4b3c13e5fed44b37b23758b81296311f712c004))

## [1.9.3](https://github.com/osl-incubator/satellite-weather-downloader/compare/1.9.2...1.9.3) (2024-02-19)


### Bug Fixes

* **downloader:** reduce from 8 to 6 days of minimum delay ([#63](https://github.com/osl-incubator/satellite-weather-downloader/issues/63)) ([766c06a](https://github.com/osl-incubator/satellite-weather-downloader/commit/766c06adbf357c05beeca5888afe2f99fc6af5ad))

## [1.9.2](https://github.com/osl-incubator/satellite-weather-downloader/compare/1.9.1...1.9.2) (2023-09-04)


### Bug Fixes

* **weather:** fix Santos SP coordinates ([#61](https://github.com/osl-incubator/satellite-weather-downloader/issues/61)) ([efadcf3](https://github.com/osl-incubator/satellite-weather-downloader/commit/efadcf33159943d76964cc30de3ed0b73a0a4482))

## [1.9.1](https://github.com/osl-incubator/satellite-weather-downloader/compare/1.9.0...1.9.1) (2023-09-04)


### Bug Fixes

* **weather:** include Santos SP coordinates ([#60](https://github.com/osl-incubator/satellite-weather-downloader/issues/60)) ([85e1827](https://github.com/osl-incubator/satellite-weather-downloader/commit/85e1827bc2d19b23ef528d2da4a8894947c1bbff))

# [1.9.0](https://github.com/osl-incubator/satellite-weather-downloader/compare/1.8.4...1.9.0) (2023-08-24)


### Features

* **downloader:** implement global fetch on satellite downloader (area) ([#59](https://github.com/osl-incubator/satellite-weather-downloader/issues/59)) ([0c8a7bc](https://github.com/osl-incubator/satellite-weather-downloader/commit/0c8a7bcc4dc4950f89026ee8c779e4618ea4541e))

## [1.8.4](https://github.com/osl-incubator/satellite-weather-downloader/compare/1.8.3...1.8.4) (2023-06-14)


### Bug Fixes

* **log:** add log to each geocode inserted ([#55](https://github.com/osl-incubator/satellite-weather-downloader/issues/55)) ([a409b26](https://github.com/osl-incubator/satellite-weather-downloader/commit/a409b26ad9eed6eff81c0936a46b59a23b2e7e9f))

## [1.8.3](https://github.com/osl-incubator/satellite-weather-downloader/compare/1.8.2...1.8.3) (2023-05-03)


### Bug Fixes

* **copebr:** remove uri and delegate connection to another script ([#54](https://github.com/osl-incubator/satellite-weather-downloader/issues/54)) ([971687e](https://github.com/osl-incubator/satellite-weather-downloader/commit/971687ee79f46c40bd236b92919f97cd6f1c71e7))

## [1.8.2](https://github.com/osl-incubator/satellite-weather-downloader/compare/1.8.1...1.8.2) (2023-04-14)


### Bug Fixes

* **v:** bumb version ([#52](https://github.com/osl-incubator/satellite-weather-downloader/issues/52)) ([992f2df](https://github.com/osl-incubator/satellite-weather-downloader/commit/992f2df1bc8833064107f560afe42c71670a5f2c))

## [1.8.1](https://github.com/osl-incubator/satellite-weather-downloader/compare/1.8.0...1.8.1) (2023-04-12)


### Bug Fixes

* **downloader:** add back cdsapi_key to download method ([#50](https://github.com/osl-incubator/satellite-weather-downloader/issues/50)) ([c270a50](https://github.com/osl-incubator/satellite-weather-downloader/commit/c270a50fa34c78423db181457f0ff4ea3ef33055))

# [1.8.0](https://github.com/osl-incubator/satellite-weather-downloader/compare/1.7.0...1.8.0) (2023-04-04)


### Features

* **version:** bumping version to 1.8 ([#49](https://github.com/osl-incubator/satellite-weather-downloader/issues/49)) ([21f55e4](https://github.com/osl-incubator/satellite-weather-downloader/commit/21f55e4f69204c8b2122425a05e856299f15f327))

# [1.7.0](https://github.com/osl-incubator/satellite-weather-downloader/compare/1.6.1...1.7.0) (2023-03-15)


### Features

* **dask:** use dask to create final df ([#47](https://github.com/osl-incubator/satellite-weather-downloader/issues/47)) ([5998dd2](https://github.com/osl-incubator/satellite-weather-downloader/commit/5998dd2bfa210dd71e5e3ca2fec7855674b60ccb))

## [1.6.1](https://github.com/osl-incubator/satellite-weather-downloader/compare/1.6.0...1.6.1) (2023-02-07)


### Bug Fixes

* **docker:** fix containers healthcheck ([#45](https://github.com/osl-incubator/satellite-weather-downloader/issues/45)) ([9ef77a7](https://github.com/osl-incubator/satellite-weather-downloader/commit/9ef77a7b513662505503b5045eb6c7e23d907071))

# [1.6.0](https://github.com/osl-incubator/satellite-weather-downloader/compare/1.5.3...1.6.0) (2023-02-01)


### Features

* **weather:** start working on Polygon Filtering ([#43](https://github.com/osl-incubator/satellite-weather-downloader/issues/43)) ([4d1526a](https://github.com/osl-incubator/satellite-weather-downloader/commit/4d1526a3c60ad6337f6480e24542010ea7d84683))

## [1.5.3](https://github.com/osl-incubator/satellite-weather-downloader/compare/1.5.2...1.5.3) (2023-01-31)


### Bug Fixes

* **imports:** package missing local import ([4369714](https://github.com/osl-incubator/satellite-weather-downloader/commit/4369714f901c34a62e39070b4c7c0e6ed1e92534))

## [1.5.2](https://github.com/osl-incubator/satellite-weather-downloader/compare/1.5.1...1.5.2) (2023-01-31)


### Bug Fixes

* **readme:** fix typo ([2be8f38](https://github.com/osl-incubator/satellite-weather-downloader/commit/2be8f3879bf7182068e5dfde839d71609faa04d9))

## [1.5.1](https://github.com/osl-incubator/satellite-weather-downloader/compare/1.5.0...1.5.1) (2023-01-31)


### Bug Fixes

* **downloader:** minor import fixes ([#39](https://github.com/osl-incubator/satellite-weather-downloader/issues/39)) ([e5fc1bd](https://github.com/osl-incubator/satellite-weather-downloader/commit/e5fc1bd8e50bb295c8aede954a72f189a6daa0d4))

# [1.5.0](https://github.com/osl-incubator/satellite-weather-downloader/compare/1.4.10...1.5.0) (2023-01-30)


### Features

* **cli:** start working in CLI menu to API request ([#37](https://github.com/osl-incubator/satellite-weather-downloader/issues/37)) ([b3b43ad](https://github.com/osl-incubator/satellite-weather-downloader/commit/b3b43ad226b410cb20ac4f73f0962f06eb2f36ae))

## [1.4.10](https://github.com/osl-incubator/satellite-weather-downloader/compare/1.4.9...1.4.10) (2023-01-26)


### Bug Fixes

* **scanner:** make scanner more flexible and remove its coupling ([#36](https://github.com/osl-incubator/satellite-weather-downloader/issues/36)) ([56e1f57](https://github.com/osl-incubator/satellite-weather-downloader/commit/56e1f57cfe04783f82308e2850aa413a398c1d55))

## [1.4.9](https://github.com/osl-incubator/satellite-weather-downloader/compare/1.4.8...1.4.9) (2023-01-25)


### Bug Fixes

* **scan:** missing path from status table ([#32](https://github.com/osl-incubator/satellite-weather-downloader/issues/32)) ([0b9a55e](https://github.com/osl-incubator/satellite-weather-downloader/commit/0b9a55e56528cbb250b2dda561d382376a345570))

## [1.4.8](https://github.com/osl-incubator/satellite-weather-downloader/compare/1.4.7...1.4.8) (2023-01-25)


### Bug Fixes

* **weather:** task was always marking as failed ([#31](https://github.com/osl-incubator/satellite-weather-downloader/issues/31)) ([7fb200e](https://github.com/osl-incubator/satellite-weather-downloader/commit/7fb200e0d67b4638861f880ac6a4dc241e4afa23))

## [1.4.7](https://github.com/osl-incubator/satellite-weather-downloader/compare/1.4.6...1.4.7) (2023-01-25)


### Bug Fixes

* **downloader:** inconsistent data scans were getting wrong values ([#30](https://github.com/osl-incubator/satellite-weather-downloader/issues/30)) ([fdde533](https://github.com/osl-incubator/satellite-weather-downloader/commit/fdde533718e64c6a3d03264ad4f8b885f6664b78))

## [1.4.6](https://github.com/osl-incubator/satellite-weather-downloader/compare/1.4.5...1.4.6) (2023-01-24)


### Bug Fixes

* **weather:** fix the raised exception when fetch task fails ([#27](https://github.com/osl-incubator/satellite-weather-downloader/issues/27)) ([59c780c](https://github.com/osl-incubator/satellite-weather-downloader/commit/59c780cfa3f68f7877c661c870929d09bbc1a181))

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
