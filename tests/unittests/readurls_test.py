import pytest
import os 
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from adaptercontroller.adapter_template import AdapterTemplate
def test_read_all_site_based_urls():
    url = 'taxjar'
    adapter = AdapterTemplate(url)
    result = adapter.read_all_site_based_urls()
    assert isinstance(result, list)
    assert len(result) > 0
    #assert all('Owner' in site and 'Website link' in site for site in result)