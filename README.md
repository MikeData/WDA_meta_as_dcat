# WDA_meta_as_dcat

Quick experiment to push some of the data from datasetDetails from the WDA API into a DCAT shaped json file, as per recommendations on:
http://guidance.data.gov.uk/dcat_fields.html

This repo includes a zip file with some 80-odd "WDA as dcat" files, which while far from exhaustive is enough for now (the script in this repo is basic and would need considerable work to capture ALL datasets in this way - it gets complicated). 

You can view any of the new files with a json viewer like this one:
http://jsoneditoronline.org/

A lot of assumptions and choices had to made and are detailed below, broken down per field:




## title
I've just used the english name.

## description
taken as-is, some cleaning of rogue html tags

## identifier
used WDA id. should be a URI but we dont have one. There's a case for using the data explorer dataset details page but
it's in multiple other fields already so seemed redundant.

##license
used OGL url. http://www.nationalarchives.gov.uk/doc/open-government-licence/version/2/

## keyword
cant find any on the API and data explorer pages dont have a traditional meta tag.
hacked dimension names into something that should do for playing around (I wouldnt recommend it for production).

## issued
used datePublished

## modified
doesent appear on the API that I can see.

## publisher 
us, general info email

## distribution
In a WDA context distribution and landingPage would seem to be something like:
distribution - http://web.ons.gov.uk/ons/data/dataset-finder/-/q/datasetView/Census/AF001EW?p_auth=8CXFEJzi&p_p_auth=fexqU0F3&p_p_lifecycle=1&_FOFlow1_WAR_FOFlow1portlet_geoTypeId=2011STATH&_FOFlow1_WAR_FOFlow1portlet_UUID=0

landingPage - http://web.ons.gov.uk/ons/data/dataset-finder/-/q/dcDetails/Census/AF001EW?p_auth=Fm6vhNuc&p_p_lifecycle=1&_FOFlow1_WAR_FOFlow1portlet_dataset_navigation=datasetCollectionDetails

BUT some dataset are too large to view directly without slicing, so err'd on the side of caution and used details page both times.

## landingPage
* see above

## references
couldnt find anything suitable so pointing to landing page the same as for publisher and distribution

## language
English. I've used the url suggested by data.gov which appears to from an american library of congress?! vocabulary. 
http://id.loc.gov/vocabulary/iso639-1/en
They seem unlikely to detail welsh.

## frequency
no data.


## temporal
You could possibly derive this from querying the "time" dimension via the API but it gets complicated.

## spatial
this is recommended as expressed in terms of co-ordinates but we tend to use pre-determined hierachies
so went with hierqrchy name, ive used either "geoitemlabel" or the name from "geoCoverage" (which one is present varies between datasets).They dont all have geography so this may also come up blank.


