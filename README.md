# Satellite Weather Downloader

| Xarray | Copernicus |
|:-------------------------:|:-------------------------:|
|<img width="1604" alt="Xarray" src="https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fxray.readthedocs.io%2Fen%2Fv0.9.0%2F_images%2Fdataset-diagram-logo.png&f=1&nofb=1&ipt=4f24c578ee40cd8ac0634231db6bd24d811fe59658eb2f5f67181f6d720d3f20&ipo=images"> |  <img width="1604" alt="Copernicus" src="https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fwww.eea.europa.eu%2Fabout-us%2Fwho%2Fcopernicus-1%2Fcopernicus-logo%2Fimage&f=1&nofb=1&ipt=56337423b2d920fcf9b4e9dee584e497a5345fc73b20775730740f0ca215fb38&ipo=images">|

SWD is a system for downloading, transforming and analysing Copernicus weather data using Xarray. The lib is split in two functionalities, `request` and the `@cope` Xarray extension. `request` is responsible for extracting NetCDF4 files from Copernicus API, and the `cope` implements Xarray extensions for transforming and visualizing the files.

## Installation
The app is available on PYPI, you can use the package without deploying the containers with the command in your shell:
``` bash
$ pip install satellite-weather-downloader
```

## Requirements
For downloading data from [Copernicus API](https://cds.climate.copernicus.eu/#!/home), it is required an account. The credentials for your account can be found in Copernicus' User Page, in the `API key` section. User API Key will be needed in order to request data, pass them to the in request's `api_key` parameter.


## Create requests via Interactive shell
```python
from satellite import request

dataset = request.reanalysis_era5_land(
    output='my_dataset_file'
    # Any ERA5 Land Reanalysis option can be passed in the method
)
```
```
NOTE: see notebooks/ to more examples
```

## Extract Brazil NetCDF4 file from a date range
``` python
dataset = request.reanalysis_era5_land(
  "bra_dataset"
  locale='BRA',
  date='2023-01-01/2023-01-07'
)

```

## Load the dataset
``` python
from satellite import DataSet
dataset = DataSet.from_netcdf("bra_dataset.zip")

```

## Usage of `cope` extension
``` python
from satellite import ADM2
rio_adm = ADM2.get(code=3304557, adm0="BRA") # Rio de Janeiro's geocode (IBGE)
dataset.cope.to_dataframe(rio_adm)
```

It is also possible to create a dataframe directly from the National-wide dataset:
``` python
rio_ds = dataset.cope.adm_ds(rio_adm)
```

All Xarray methods are extended when using the `copebr` extension:
``` python
rio_ds.precip_tot.to_array()
rio_ds.temp_med.plot()
```

## Metodologia Mosqlimate

A metodologia implementada no pacote `satellite-weather-downloader` para agregar dados do satélite ERA5 a nível municipal, que alimenta o Mosqlimate, segue as etapas:

* **Dados de Entrada**: Arquivos `netCDF4` provenientes da API da Copernicus, contendo dados brutos de reanálise climática.
* **Conversão de Unidades e Cálculo de Variáveis**:
    * **Temperatura (`t2m`)**: Convertida de Kelvin (K) para Graus Celsius (°C).
    * **Umidade Relativa (`umid`)**: Calculada a partir da temperatura do ar a 2m (`t2m`) e da temperatura do ponto de orvalho a 2m (`d2m`), ambas em °C. O resultado é expresso em porcentagem (%).
    * **Precipitação Total (`tp`)**: Convertida de metros (m) para milímetros (mm).
    * **Pressão Superficial (`sp`)**: Convertida de Pascals (Pa) para atmosferas (atm) utilizando o fator de conversão 0.00000986923.
    * As variáveis são renomeadas para um formato padronizado (ex: `t2m` para `temp`, `tp` para `precip`, `d2m` para `umid`, `sp` para `pressao`).
* **Agregação Espacial (Estatísticas Zonais)**:
    * Utiliza a biblioteca `xagg` do Python.
    * `xa.pixel_overlaps()`: Calcula um mapa de pesos que representa a fração de cada pixel da grade do satélite que se sobrepõe à geometria de cada município. Isso assegura uma ponderação pela área na agregação.
    * `xa.aggregate()`: Agrega os dados do satélite para cada município utilizando os pesos calculados. (Esta agregação ocorre sobre os dados na sua resolução temporal original, por exemplo, horária).
* **Agregação Temporal Diária**:
    * `ds.resample(time="1D")`: Os dados agregados espacialmente (e ainda na resolução temporal original) são reamostrados para uma frequência diária.
    * Para cada dia e município, são calculadas as seguintes estatísticas a partir da série temporal reamostrada:
        * Mínimo (sufixo `_min`)
        * Média (sufixo `_med`)
        * Máximo (sufixo `_max`)
        * Soma (sufixo `_tot`, especificamente para precipitação: `precip_tot`)
* **Formato de Saída**:
    * Os dados são estruturados em um `pandas.DataFrame`.
    * Inclui colunas como `date` (data), `geocode` (código do município), e `epiweek` (semana epidemiológica calculada a partir da data).
    * Valores numéricos das variáveis climáticas são arredondados (ex: 4 casas decimais).

## Mosqlimate Methodology

The methodology implemented in the `satellite-weather-downloader` package to aggregate ERA5 satellite data at the municipal level, which feeds Mosqlimate, follows these steps:

* **Input Data**: `netCDF4` files from the Copernicus API, containing raw climate reanalysis data.
* **Unit Conversion and Variable Calculation**:
    * **Temperature (`t2m`)**: Converted from Kelvin (K) to Degrees Celsius (°C).
    * **Relative Humidity (`umid`)**: Calculated from the 2m air temperature (`t2m`) and the 2m dew point temperature (`d2m`), both in °C. The result is expressed as a percentage (%).
    * **Total Precipitation (`tp`)**: Converted from meters (m) to millimeters (mm).
    * **Surface Pressure (`sp`)**: Converted from Pascals (Pa) to atmospheres (atm) using the conversion factor 0.00000986923.
    * Variables are renamed to a standardized format (e.g., `t2m` to `temp`, `tp` to `precip`, `d2m` to `umid`, `sp` to `pressao`).
* **Spatial Aggregation (Zonal Statistics)**:
    * Uses the Python `xagg` library.
    * `xa.pixel_overlaps()`: Calculates a weight map representing the fraction of each satellite grid pixel that overlaps with the geometry of each municipality. This ensures area-weighted aggregation.
    * `xa.aggregate()`: Aggregates satellite data for each municipality using the calculated weights. (This aggregation occurs on the data at its original temporal resolution, e.g., hourly).
* **Daily Temporal Aggregation**:
    * `ds.resample(time="1D")`: The spatially aggregated data (still at its original temporal resolution) is resampled to a daily frequency.
    * For each day and municipality, the following statistics are calculated from the resampled time series:
        * Minimum (suffix `_min`)
        * Mean (suffix `_med`)
        * Maximum (suffix `_max`)
        * Sum (suffix `_tot`, specifically for precipitation: `precip_tot`)
* **Output Format**:
    * Data is structured into a `pandas.DataFrame`.
    * Includes columns such as `date`, `geocode` (municipality code), and `epiweek` (epidemiological week calculated from the date).
    * Numerical values of climate variables are rounded (e.g., to 4 decimal places).
