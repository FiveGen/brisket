from BeautifulSoup import BeautifulSoup
from django.conf import settings
import helpers
import urllib2
import urllib
import re
try:
    import json
except:
    import simplejson as json


API_BASE_URL = settings.AGGREGATES_API_BASE_URL.strip('/')+'/'

# defaults of None don't mean that there is not default or no limit--
# it means that no parameter will be sent to the server, and the server
# will use its own default.
DEFAULT_CYCLE = "-1" # -1 will return career totals.
DEFAULT_LIMIT = None


def remove_unicode(data):
    ''' converts a dictionary or list of dictionaries with unicode
    keys or values to plain string keys'''
    if isinstance(data, dict):
        plain = {}
        for k,v in data.iteritems():
            k = remove_unicode(k)
            v = remove_unicode(v)
            plain[k] = v
        return plain
    if isinstance(data, list):
        plain = []
        for record in data:
            plain.append(remove_unicode(record))
        return plain
    if isinstance(data,unicode):
        return str(data)
    else: return data


def get_url_json(path, cycle=None, limit=None, **params):
    """ Low level call that just adds the API key, retrieves the URL and parses the JSON. """

    if cycle:
        params.update({'cycle': cycle})
    if limit:
        params.update({'limit': limit})
    params.update({'apikey': settings.API_KEY})

    fp = urllib2.urlopen(API_BASE_URL + path + '?' + urllib.urlencode(params))
    results = json.loads(fp.read())
    return remove_unicode(results)


def entity_search(query):
    return get_url_json('entities.json', search=query)


def entity_metadata(entity_id, cycle=DEFAULT_CYCLE):
    results = get_url_json('entities/%s.json' % entity_id, cycle)
    career = results['totals'].keys()
    career.sort()
    # start at index 1 to skip over the -1 for 'all cycles'
    if len(career):
        results['career'] = {'start': career[1], 'end': career[-1]}
    else:
        results['career'] = {}

    # lobbying career
    lobbying_career = [k for (k,v) in results['totals'].items() if v['lobbying_count']]
    lobbying_career.sort()
    # start at index 1 to skip over the -1 for 'all cycles'
    if len(lobbying_career):
        results['lobbying_career'] = {'start': lobbying_career[1], 'end': lobbying_career[-1]}
    else:
        results['lobbying_career'] = {}

    return results


def entity_id_lookup(namespace, id):
    return get_url_json('entities/id_lookup.json', namespace=namespace, id=id)


def pol_contributors(entity_id, cycle=DEFAULT_CYCLE, limit=DEFAULT_LIMIT):
    return get_url_json('aggregates/pol/%s/contributors.json' % entity_id, cycle, limit)


def indiv_org_recipients(entity_id, cycle=DEFAULT_CYCLE, limit=DEFAULT_LIMIT):
    ''' recipients from a single individual'''
    return get_url_json('aggregates/indiv/%s/recipient_orgs.json' % entity_id, cycle, limit)


def indiv_pol_recipients(entity_id, cycle=DEFAULT_CYCLE, limit=DEFAULT_LIMIT):
    ''' recipients from a single individual'''
    return get_url_json('aggregates/indiv/%s/recipient_pols.json' % entity_id, cycle, limit)


def org_recipients(entity_id, cycle=DEFAULT_CYCLE, limit=DEFAULT_LIMIT):
    return get_url_json('aggregates/org/%s/recipients.json' % entity_id, cycle, limit)


def pol_sectors(entity_id, cycle=DEFAULT_CYCLE, limit=DEFAULT_LIMIT):
    return get_url_json('aggregates/pol/%s/contributors/sectors.json' % entity_id, cycle, limit)


def org_industries_for_sector(entity_id, sector_id, cycle=DEFAULT_CYCLE, limit=DEFAULT_LIMIT):
    return get_url_json('aggregates/pol/%s/contributors/sector/%s/industries.json' % (entity_id, sector_id), cycle, limit)


def org_party_breakdown(entity_id, cycle=DEFAULT_CYCLE):
    return get_url_json('aggregates/org/%s/recipients/party_breakdown.json' % entity_id, cycle)


def org_level_breakdown(entity_id, cycle=DEFAULT_CYCLE):
    return get_url_json('aggregates/org/%s/recipients/level_breakdown.json' % entity_id, cycle)


def pol_local_breakdown(entity_id, cycle=DEFAULT_CYCLE):
    return get_url_json('aggregates/pol/%s/contributors/local_breakdown.json' % entity_id, cycle)


def pol_contributor_type_breakdown(entity_id, cycle=DEFAULT_CYCLE):
    return get_url_json('aggregates/pol/%s/contributors/type_breakdown.json' % entity_id, cycle)


def indiv_party_breakdown(entity_id, cycle=DEFAULT_CYCLE):
    return get_url_json('aggregates/indiv/%s/recipients/party_breakdown.json' % entity_id, cycle)

# lobbying firms hired by this org
def org_registrants(entity_id, cycle=DEFAULT_CYCLE, limit=DEFAULT_LIMIT):
    ''' check to see if the entity hired any lobbyists'''
    return get_url_json('aggregates/org/%s/registrants.json' % entity_id, cycle, limit)

# issues this org hired lobbying for
def org_issues(entity_id, cycle=DEFAULT_CYCLE, limit=DEFAULT_LIMIT):
    return get_url_json('aggregates/org/%s/issues.json' % entity_id, cycle, limit)

# lobbyists who lobbied for this org (?)
def org_lobbyists(entity_id, cycle=DEFAULT_CYCLE, limit=DEFAULT_LIMIT):
    return get_url_json('aggregates/org/%s/lobbyists.json' % entity_id, cycle, limit)

# which lobbying firms did this indiv work for
def indiv_registrants(entity_id, cycle=DEFAULT_CYCLE, limit=DEFAULT_LIMIT):
    return get_url_json('aggregates/indiv/%s/registrants.json' % entity_id, cycle, limit)

# issues this individual lobbied on
def indiv_issues(entity_id, cycle=DEFAULT_CYCLE, limit=DEFAULT_LIMIT):
    return get_url_json('aggregates/indiv/%s/issues.json' % entity_id, cycle, limit)

# who were the clients of the firms this indiv worked for
def indiv_clients(entity_id, cycle=DEFAULT_CYCLE, limit=DEFAULT_LIMIT):
    return get_url_json('aggregates/indiv/%s/clients.json' % entity_id, cycle, limit)

# issues this org was hired to lobby for
def org_registrant_issues(entity_id, cycle=DEFAULT_CYCLE, limit=DEFAULT_LIMIT):
    return get_url_json('aggregates/org/%s/registrant/issues.json' % entity_id, cycle, limit)

# clients of the org as a registrant
def org_registrant_clients(entity_id, cycle=DEFAULT_CYCLE, limit=DEFAULT_LIMIT):
    return get_url_json('aggregates/org/%s/registrant/clients.json' % entity_id, cycle, limit)

# lobbyists who work for this registrant (?)
def org_registrant_lobbyists(entity_id, cycle=DEFAULT_CYCLE, limit=DEFAULT_LIMIT):
    return get_url_json('aggregates/org/%s/registrant/lobbyists.json' % entity_id, cycle, limit)


# top n lists
def top_n_individuals(cycle=DEFAULT_CYCLE, limit=DEFAULT_LIMIT):
    return get_url_json('aggregates/indivs/top_%s.json' % limit, cycle)

def top_n_organizations(cycle=DEFAULT_CYCLE, limit=DEFAULT_LIMIT):
    return get_url_json('aggregates/orgs/top_%s.json' % limit, cycle)

def top_n_politicians(cycle=DEFAULT_CYCLE, limit=DEFAULT_LIMIT):
    return get_url_json('aggregates/pols/top_%s.json' % limit, cycle)


def org_sparkline(entity_id, cycle=DEFAULT_CYCLE):
    return get_url_json('aggregates/org/%s/sparkline.json' % entity_id, cycle)

def org_sparkline_by_party(entity_id, cycle=DEFAULT_CYCLE):
    return  get_url_json('aggregates/org/%s/sparkline_by_party.json' % entity_id, cycle)

def pol_sparkline(entity_id, cycle=DEFAULT_CYCLE):
    return get_url_json('aggregates/pol/%s/sparkline.json' % entity_id, cycle)

def indiv_sparkline(entity_id, cycle=DEFAULT_CYCLE):
    return get_url_json('aggregates/indiv/%s/sparkline.json' % entity_id, cycle)

def pairwise_amount(pol_id, org_id):
    return get_url_json('aggregates/recipient/%s/contributor/%s/amount.json' % (pol_id, org_id))

def politician_meta(entity_id):
    metadata = entity_metadata(entity_id)

    bioguide_id = None
    if metadata and metadata['metadata']['bioguide_id']:
        bioguide_id = metadata['metadata']['bioguide_id']
    else:
        return None

    # scrape congress's bioguide site for years of service and official bio
    html = urllib2.urlopen("http://bioguide.congress.gov/scripts/biodisplay.pl?index=%s" % bioguide_id).read()
    soup = BeautifulSoup(html, convertEntities=BeautifulSoup.HTML_ENTITIES)
    yrs_of_service = soup.findAll('table')[1].find('tr').findAll('td')[1].findAll('font')[2].next.next.next.strip()
    bio_a = soup.findAll('table')[1].find('tr').findAll('td')[1].find('p').find('font').extract().renderContents()
    bio_b = soup.findAll('table')[1].find('tr').findAll('td')[1].find('p').renderContents()
    biography = bio_a.strip()+' '+bio_b.strip()

    # other metadata - from sunlightlabs services
    arguments = urllib.urlencode({'apikey': settings.API_KEY,
                                  'bioguide_id': bioguide_id,
                                  'all_legislators': 1,
                                  })
    url = "http://services.sunlightlabs.com/api/legislators.get.json?"
    api_call = url + arguments
    print api_call
    fp = urllib2.urlopen(api_call)
    js = json.loads(fp.read())
    meta = js['response']['legislator']

    # append additional info and return
    meta['photo_url'] = metadata['metadata']['photo_url']
    meta['yrs_of_service'] = yrs_of_service
    meta['biography'] = biography
    return meta


