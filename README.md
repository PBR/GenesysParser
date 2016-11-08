# GenesysParser

This project acts as an intermediate layer between the Genesys PGR API 
and an application that utilises its data. It is intended to both facilitate 
the query setup, as well as automate a big part of the response collection.

## Requirements

The project runs on Python 2.7+ and Python 3.2+.  
Libraries required:

* requests (`pip install requests`)

## Example use

The file `main.py` showcases the use of the GenesysRequest class. The
steps to follow are outlined below.

### 1. Providing the basic configuration
A template file titled `config.py-example` can be edited for this purpose, to 
produce `config.py`. The parameters that must be specified are:

* `url`: the base address of the site to be queried. There are currently two 
possibilities for this, 
the official Genesys site ([https://www.genesys-pgr.org/](https://www.genesys-pgr.org/)), and
the Genesys sandbox site ([https://sandbox.genesys-pgr.org/](https://sandbox.genesys-pgr.org/)).
The `/` terminator is optional.

* `clientID` and `clientSecret`: The string credentials as given by the site. It is
worth noting that they are not cross-compatible, so they must be for the respective site.

In `config.py-example`, edit the strings as necessary without altering the variable names.
Then rename the file to `config.py`, and leave it in the same directory.


### 2. Setting up the query
First, the query parameters need to be defined. This is done by means of
a dictionary, the keys for which are listed 
[here](https://gitlab.croptrust.org/genesys-pgr/genesys-server/blob/13969d3caa1632bfc0994d6148ebfaa933e6da7b/src/main/java/org/genesys2/server/service/FilterConstants.java)
as:
```
crops 
sampStat 
storage 
coll.collMissId 
available 
art15 
mlsStatus 
sgsv 
alias 
acceNumb 
institute.code 
geo.elevation 
geo.longitude 
geo.latitude 
orgCty.iso3 
taxonomy.sciName 
taxonomy.species 
taxonomy.genus 
taxonomy.subtaxa 
id 
duplSite 
donorCode 
institute.country.iso3 
institute.country.iso2 
institute.networks 
inSgsv 
taxonomy.genusSpecies 
historic 
seqNo 
lists
```
Further information about these fields can be found 
[here](https://gitlab.croptrust.org/genesys-pgr/genesys-server/blob/5381dd7fb9d4af2e2e4dabb4e7b1b8a2612af206/src/main/asciidoc/sections/mcpd.adoc).
Additionally, the institute codes, among other details, can be found on the 
[WIEWS homepage](http://www.fao.org/wiews-archive/wiewspage.jsp?i_l=@@&show=DownloadinstEN.jsp).

Don't forget to include the class:
```python
from GenesysRequest import GenesysRequest
```

Using the above, the query parameters for a few types of tomato, at the institutes
 as seen below would be:
```python
query_params = \
    {
        'institute.code':
            [
                'NLD037',  # CGN
                'USA003',  # Geneva
                'DEU146',  # Gatersleben
                'USA176',  # Tomato Genetics Resource Center
            ],
            'taxonomy.genus': ['Solanum', 'Lycopersicon'],
            'taxonomy.species': ['lycopersicum', 'esculentum', 'sp.',
                                 'pimpinellifolium', 'peruvianum'],
    }
```
Following the definition of the query parameters, instantiation of the class
is simple:
```python
r = GenesysRequest(query_params)
```

### 3. Submitting the query
Once the query parameters have been specified, the query may be submitted to the site.
There are two ways to do this, depending on one's needs.

#### Fetching a specific page/number of results
`r.submitReq()` will only fetch one page of results. The function takes two parameters:

`r.submitReq(page, size)`, set by default to 1 (the first page of results) and 50 respectively.
50 is also the maximum number of result items the site allows per query, which means that queries
with a larger number of results must be submitted as multiple requests to the site.

Example uses: `r.submitReq()`, `r.submitReq(1)`,`r.submitReq(size=10)`, `r.submitReq(page=1, size=10)`.
The first and second examples both fetch the first page of results, with a maximum of 50 items.
The third and fourth examples also fetches the first page, but with a maximum result size of 10 items.

#### Fetching all results at once
As many query results might be composed of multiple pages, the `fetchall()` function is provided.
It will fetch as many pages as necessary to exhaust all results. As it is intended to provide a complete
list of results without an unnecessary number of queries, this function takes no `page` or `size` parameters.

Example use: `r.fetchAll()`.

### 4. Iterating through the results

The result of a query submitted in the way described above is a list of `ItemGenesys` objects.
The `full` field of this class holds the MCPD of each result item in its entirety, and its sub-fields
are accessible as parts of a python dictionary.  
The most commonly used fields are also accessible directly, as class attributes. These are:
```
genesysUUID, acqDate, accessionID, collectionDate, genus, species, collSite, instituteCode, aliases
````
It is worth mentioning that the acqDate, as a class attribute, undergoes some processing and is available
as a datetime.date object. In particular, as Genesys uses the '00' or '--' notation when a field of (year, month, day)
is unavailable, the class substitutes these with the defaults of (`0001`, `01`, `01`) respectively.

For example, it is possible to print all accession IDs of the results in the two following ways:

```python
for result_item in r.fetchAll():
    print(result_item.full['acceNumb'])
```

or

```python
for result_item in r.fetchAll():
    print(result_item.accessionID)
```

It is also possible to print a result item, as a product of its most commonly used fields, as follows:
```python
print(result_item)
```

which results in this description for [PI 100697](https://www.genesys-pgr.org/1/acn/id/176452):
```python
ItemGenesys(accessionID=PI 100697, collectionDate=1932-06-28, otherNames=[321], genus=Solanum, species=lycopersicum, instituteCode=USA003, collectionSite=None)
```


Further examples can be found at the end of `GenesysRequest.py`.

### Side notes
#### Logging
Several logging parameters can be adjusted in `logging.json`. By default, all
messages are set to show as well as be recorded in the `debug.log` and `errors.log` files.

#### curl request
The `curl` command to directly query the Genesys API using a 
`clientID` and `clientSecret` for the accession number `PI 100697` would look like:

```sh
curl -H 'Content-Type: application/json' -H 'Referer: http://ecpgr.cgn.wur.nl/eupotato/test.html' -X POST -d '{"filter": "{\"acceNumb\":[\"PI 100697\"]}"}' 'https://sandbox.genesys-pgr.org/webapi/v0/acn/filter?client_id=clientID&client_secret=clientSecret'
```
and produce a result like [this](http://pastebin.com/DA7ffDBa).

