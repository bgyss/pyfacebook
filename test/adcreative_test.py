from pyfacebook.settings import FACEBOOK_APP_SECRET
from pyfacebook.settings import FACEBOOK_APP_ID
from pyfacebook.settings import FACEBOOK_TEST_ACCESS_TOKEN
from pyfacebook.settings import FACEBOOK_TEST_ACCOUNT_ID
from pyfacebook.settings import FACEBOOK_PROD_ACCOUNT_ID

from pyfacebook import PyFacebook

from nose.tools import eq_, ok_


class TestAdCreativeApi():

    def setUp(self):
        self.fb = PyFacebook(app_id=FACEBOOK_APP_ID,
                             access_token=FACEBOOK_TEST_ACCESS_TOKEN,
                             app_secret=FACEBOOK_APP_SECRET)

    def test_find_by_adaccount_id(self):
        # Check order
        first_ten_adcreatives = self.fb.api().adcreative().find_by_adaccount_id(FACEBOOK_PROD_ACCOUNT_ID, limit=10, offset=0)
        second_five_adcreatives = self.fb.api().adcreative().find_by_adaccount_id(FACEBOOK_PROD_ACCOUNT_ID, limit=5, offset=5)

        eq_(len(first_ten_adcreatives), 10)
        eq_(len(second_five_adcreatives), 5)

        for c in first_ten_adcreatives[5:]:
            index = first_ten_adcreatives.index(c) - 5
            eq_(c.id, second_five_adcreatives[index].id)

        # Check attributes
        adcreative = c
        ok_(not not adcreative.body)
        ok_(not not adcreative.name)
        ok_(not not adcreative.link_url)
        ok_(not not adcreative.title)

        # Check completeness of paged results
        all_creatives = self.fb.api().adcreative().find_by_adaccount_id(FACEBOOK_PROD_ACCOUNT_ID)
        total = len(all_creatives)

        limit = 3
        offset = total - limit + 1
        last_batch_of_creatives = self.fb.api().adcreative().find_by_adaccount_id(FACEBOOK_PROD_ACCOUNT_ID, limit=limit, offset=offset)
        eq_(len(last_batch_of_creatives), total - offset)

        # Check empty results
        no_creatives = self.fb.api().adcreative().find_by_adaccount_id(FACEBOOK_PROD_ACCOUNT_ID, offset=total)
        eq_(no_creatives, [])

        # Check full results
        offset = 0
        all_creatives = self.fb.api().adcreative().find_by_adaccount_id(FACEBOOK_PROD_ACCOUNT_ID, offset=offset, limit=total + 1000)
        eq_(len(all_creatives), total)

    def test_find_by_adgroup_id(self):
        adgroups = self.fb.api().adgroup().find_by_adaccount_id(FACEBOOK_TEST_ACCOUNT_ID, limit=2)
        adgroup = adgroups[0]

        adcreatives = self.fb.api().adcreative().find_by_adgroup_id(adgroup.id)
        adcreative = adcreatives[0]

        ok_(not not adcreative.name)
        ok_(not not adcreative.type)
        ok_(not not adcreative.action_spec)

    def test_find_by_ids(self):
        base_adcreatives = self.fb.api().adcreative().find_by_adaccount_id(FACEBOOK_TEST_ACCOUNT_ID, limit=25)

        # Test pulling 10 adcreatives
        test_adcreative_ids = map(lambda x: x.id, base_adcreatives)  # cool way of pulling a simple list of attributes from a list of more complex objects
        adcreatives = self.fb.api().adcreative().find_by_ids(test_adcreative_ids[:10])
        result_adcreative_ids = map(lambda x: x.id, adcreatives)

        eq_(10, len(adcreatives))
        ok_(test_adcreative_ids[0] in result_adcreative_ids)

        # Test empty adcreative_ids error
        try:
            adcreatives = self.fb.api().adcreative().find_by_ids([])
        except Exception, e:
            eq_(e.message, "A list of ids is required")
