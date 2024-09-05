import pytest
import os 
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from adaptercontroller.adapter_template import AdapterTemplate
def test_read_all_site_based_urls():
    url = 'taxjar'
    adapter = AdapterTemplate(url)
    adapter.read_all_site_based_urls()
    result = adapter.scrap_webiste()
   
    assert result == True
    #assert all('Owner' in site and 'Website link' in site for site in result)