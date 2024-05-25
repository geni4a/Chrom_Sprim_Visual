# Chrom_Sprim_Visual
This tool aids in S Prime analysis by providing pairwise comparision visual tools. This is helpful in figuring out which populations have more common shared ancestry based on proportion of shared introgressed segments.


## Activate virtual environment
python3 -m venv env

source env/bin/activate

## Packages that need to be installed
To install packages, you can use pip or pip 3

```
pip3 install -r requirements.txt 
```

Make sure the location to which packages are installed are on PATH
```
export PATH=/path/to/directory:$PATH
```

## If not using own files
- Clone repository
- Locate directory 

type 
```
  bokeh serve --show .

```


if facing issues even after installing the necessary packages, 
type 
```
  python -m bokeh serve --show .

```
  or
  ```
  python3 -m bokeh serve --show .

```

- To view how preprocessing and analysis was done, check the Jupyter_Deliverables folder for the Overall_finale jupyter notebooks
  


## Format of input files

### Sprime files
- Sprime files should have population name and chromosome name included in filename
### Json file
- Ensure population names are stored in a json file




### Populations and codes

  CHB	Han Chinese             Han Chinese in Beijing, China
  JPT	Japanese                Japanese in Tokyo, Japan
  CHS	Southern Han Chinese    Han Chinese South
  CDX	Dai Chinese             Chinese Dai in Xishuangbanna, China
  KHV	Kinh Vietnamese         Kinh in Ho Chi Minh City, Vietnam
  CHD	Denver Chinese          Chinese in Denver, Colorado (pilot 3 only)

  CEU	CEPH                    Utah residents (CEPH) with Northern and Western European ancestry 
  TSI	Tuscan                  Toscani in Italia 
  GBR	British                 British in England and Scotland 
  FIN	Finnish                 Finnish in Finland 
  IBS	Spanish                 Iberian populations in Spain 

  YRI	Yoruba                  Yoruba in Ibadan, Nigeria
  LWK	Luhya                   Luhya in Webuye, Kenya
  GWD	Gambian                 Gambian in Western Division, The Gambia 
  MSL	Mende                   Mende in Sierra Leone
  ESN	Esan                    Esan in Nigeria

  ASW	African-American SW     African Ancestry in Southwest US  
  ACB	African-Caribbean       African Caribbean in Barbados
  MXL	Mexican-American        Mexican Ancestry in Los Angeles, California
  PUR	Puerto Rican            Puerto Rican in Puerto Rico
  CLM	Colombian               Colombian in Medellin, Colombia
  PEL	Peruvian                Peruvian in Lima, Peru

  GIH	Gujarati                Gujarati Indian in Houston, TX
  PJL	Punjabi                 Punjabi in Lahore, Pakistan
  BEB	Bengali                 Bengali in Bangladesh
  STU	Sri Lankan              Sri Lankan Tamil in the UK
  ITU	Indian                  Indian Telugu in the UK




## Once done, deactivate environment
deactivate