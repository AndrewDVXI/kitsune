from nose.tools import eq_

from pyquery import PyQuery as pq

from kitsune.sumo.helpers import urlparams
from kitsune.sumo.tests import LocalizingClient
from kitsune.sumo.urlresolvers import reverse
from kitsune.search.tests import ElasticTestCase


class TopContributorsNewTest(ElasticTestCase):
    """Tests for the Community Hub user search page."""
    client_class = LocalizingClient

    def test_it_works(self):
        url = reverse('community.top_contributors_new', args=['l10n'])
        res = self.client.get(url)
        eq_(res.status_code, 200)

    def test_no_xss(self):
        bad_string = 'locale=en-US8fa4a<%2fscript><script>alert(1)<%2fscript>'
        escaped_version = 'locale=en-US8fa4a<\/script><script>alert(1)<\/script>'

        url = reverse('community.top_contributors_new', args=['l10n'])
        url = urlparams(url, locale=bad_string)
        res = self.client.get(url)
        eq_(res.status_code, 200)

        doc = pq(res.content)
        target = doc('script[name="contributor-data"]')
        assert bad_string not in target.html()
        assert escaped_version in target.html()
