# -*- coding: utf-8 -*-
"""
Created on Thu Sep 29 07:37:13 2016

@author: Mike

Script to take create representative metadata json file from WDA.

Based on basic data.gov DCAT/json recommentation:
http://guidance.data.gov.uk/dcat_fields.html

Uses .xml and beautiful soup to get where we're going.
Uses .json and DICTS when we're matching up data (meta_file[title] = source[name] etc)

"""

import json
import sys
import requests
from bs4 import BeautifulSoup

DELETE_ME_LATER = []


base = 'http://data.ons.gov.uk/ons/api/data/'
context = 'Economic'

"""
REMEMBER THIS IS JUST ECONOMIC
"""

""" Get .json datasetDetails for every dataset """
contexts = ['Social', 'Economic']

for context in contexts:
    
    url = 'http://data.ons.gov.uk/ons/api/data//datasets.xml?context=%s&apikey=Y6Xs59zXU0' % (context)
    print url
    r  = requests.get(url)
    
    # Parse it, get rid of any not detail .json links
    soup = BeautifulSoup(r.content)
    all_details = soup.find_all('url', {'representation':'json'})
    all_details = [x.text for x in all_details if 'datasetdetails' in x.text]

    
    """ Then one a at a time """
    for one_detail in all_details:
        
    
            # Get the details    
            url = base = 'http://data.ons.gov.uk/ons/api/data/' + one_detail
            data = requests.get(url)
            json_as_dict = json.loads(data.text)    
        
                         
            # saving me some typing    
            json_as_dict = json_as_dict['ons']['datasetDetail']
            
            # Set basic DCAT keys, We'll add later as needed
            meta_file = {
                        'title':'',
                        'description':'',
                        'identifier':'',
                        'license':'',
                        'keyword':'',
                        'issued':'',
                        'modified':'',
                        'publisher':'',
                        'distribution':'',
                        'landingPage':'',
                        'references':'',
                        'language':'',
                        'frequency':'',
                        'temporal':'',
                        'spatial':'',
                        'theme':'',
            }
        
            # Getting what we need from datasetDetails
            # Title - assuming we want the english name
            meta_file['title'] = json_as_dict['names']['name'][0]['$']
            
            # Description (need to clean <p></p> tags out of some)
            try:
                try:
                    desc = json_as_dict['refMetadata']['refMetadataItem']['descriptions']['description'][0]['$']
                except:
                    desc = json_as_dict['refMetadata']['refMetadataItem'][0]['descriptions']['description'][0]['$']
                    # salkda = raw_input('asda')
                cleanme = ['<p>', '</p>']
                for issue in cleanme:    
                    desc = unicode(desc).replace(issue, '')
                meta_file['description'] = desc.strip()
            except:
                faildesc = json_as_dict 
            
            # Identifier
            meta_file['identifier'] = json_as_dict['id']
            
            # licence - open government licence
            meta_file['license'] = 'http://www.nationalarchives.gov.uk/doc/open-government-licence/version/2/'
            
            # keywords
            # ==========================================================================
            # TODO - very very hacky
            rubbish = ['Area','Decile','Financial Instrument','Entity Type','Growth Period','Geographic Area','Type','Membership Type','Status',
            'Direction','Legal status','Hours','Special Aggregate','Time','Value / Volume','Year', 'Component']
    
            # 1 for 1 changes
            change = {
                      'Prodcom Sales':'Prodcom',
                      'Prodcom Elements':'Prodcom',
                      'Flow of Travel':'Travel'
                      }
            
            # 1 for 2 or more changes
            changes = {
                      'SA / NSA':['Seasonally Adjusted','Non-Seasonally Adjusted'],
                      'Seasonally Adjusted / Non-Seasonally Adjusted':['Seasonally Adjusted','Non-Seasonally Adjusted'],
                      'Public / Private Sector':['Public Sector', 'Private Sector'],
                      }
    
            dims = [str(x['dimensionTitles']['dimensionTitle'][0]['$']) for x in json_as_dict['dimensions']['dimension'] if x not in rubbish]
            dims = [x for x in dims if x not in rubbish]
            
            if 'Time' in dims:
                checkme = json_as_dict
    
            # make some changes        
            for key in change.keys():
                if key in dims:
                    dims.append(change[key])
            
            for key in changes.keys():
                if key in dims:
                    for item in changes[key]:
                        dims.append(item)
                        
            # clean out the source
            dims = [x for x in dims if x not in change.keys()]
            dims = [x for x in dims if x not in changes.keys()]
                
            for x in dims:
                DELETE_ME_LATER.append(x)
            
            meta_file['keyword'] = dims
            # ==========================================================================
            
            
            # issued
            meta_file['issued'] = json_as_dict['publicationDate'][:10] # 1st 10 characters, should clean out the rubbish
            
            # publisher
            meta_file['publisher'] = {"name": "Office for National Statistics", "mbox": "info@ons.gsi.gov.uk"}
            
            # spacial, skip it if theres no label
            try:
                try:
                    meta_file['spatial'] = json_as_dict['geogItemLabel']
                except:
                    meta_file['spatial'] = json_as_dict['geocoverage'][0]['$']
            except:
                meta_file['spatial'] = json_as_dict['geocoverages']['geocoverage'][0]['$']              
                
            # language
            meta_file['language'] = 'http://id.loc.gov/vocabulary/iso639-1/en'
                
            """
            Pointing to data explorer main dataset page. See accompanying notes.
            
            """
            # distribution
            meta_file['distribution'] = 'http://web.ons.gov.uk/ons/data/dataset-finder/-/q/dcDetails/%s/%s?p_auth=Fm6vhNuc&p_p_lifecycle=1&_FOFlow1_WAR_FOFlow1portlet_dataset_navigation=datasetCollectionDetails' % (context, json_as_dict['id'])
        
            # landing oage
            meta_file['landingPage'] = 'http://web.ons.gov.uk/ons/data/dataset-finder/-/q/dcDetails/%s/%s?p_auth=Fm6vhNuc&p_p_lifecycle=1&_FOFlow1_WAR_FOFlow1portlet_dataset_navigation=datasetCollectionDetails' % (context, json_as_dict['id'])
        
            # refereences
            meta_file['references'] = 'http://web.ons.gov.uk/ons/data/dataset-finder/-/q/dcDetails/%s/%s?p_auth=Fm6vhNuc&p_p_lifecycle=1&_FOFlow1_WAR_FOFlow1portlet_dataset_navigation=datasetCollectionDetails' % (context, json_as_dict['id'])
        
            # replace stupid naming
            filename = unicode(meta_file['title']).replace('/', '-')        
        
            # create a local JSON dump out of the scrape
            with open(filename + '.json', 'wb') as fp:
                json.dump(meta_file, fp)
            fp.close()
    
