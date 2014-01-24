import random
import pytz
import datetime
import calendar
import json
from dateutil import parser as date_parser
from tinymodel import TinyModel, FieldDef
from collections import namedtuple

unix_datetime_translators = {
    'to_json': lambda obj: calendar.timegm(datetime.datetime.utcfromtimestamp(obj.utctimetuple())),
    'from_json': lambda json_value: datetime.datetime.utcfromtimestamp(long(json_value)),
    'random': lambda: (datetime.datetime.utcnow() - datetime.timedelta(seconds=random.randrange(2592000))).replace(tzinfo=pytz.utc),
}


class FacebookModel(TinyModel):

    """
    Represents a model defined by Facebook. See documentation at:
    https://developers.facebook.com/docs/ads-api/

    There should be a 1-to-1 correspondence to the Facebook model definitions,
    with the notable exception of "connections" which we defined as model fields but Facebook does not.

    """
    pass


class SupportModel(TinyModel):

    """
    Represents models which Facebook uses, but do not have their own endpoints.
    These models generally don't have their own page in the Facebook documentation,
    but are mentioned or implied in the documentation of other models.

    """
    pass


class Token(SupportModel):

    """
    Represents an oauth token for the Facebook Graph API.
    Fields are taken mostly from the return structure of the debug_token call documented at:
    https://developers.facebook.com/docs/facebook-login/access-tokens/#debug

    """
    FIELD_DEFS = [
        FieldDef(title='text', allowed_types=[unicode]),
        FieldDef(title='app_id', allowed_types=[unicode]),
        FieldDef(title='is_valid', allowed_types=[bool]),
        FieldDef(title='application', allowed_types=[unicode]),
        FieldDef(title='user_id', allowed_types=[unicode]),
        FieldDef(title='issued_at', allowed_types=[datetime.datetime], custom_translators=unix_datetime_translators),
        FieldDef(title='expires_at', allowed_types=[datetime.datetime], custom_translators=unix_datetime_translators),
        FieldDef(title='scopes', allowed_types=[[unicode], [unicode]]),
    ]


class AdImage(FacebookModel):

    """
    Represents an adimage object in the Facebook Ads API:
    https://developers.facebook.com/docs/reference/ads-api/adimage/

    """
    FIELD_DEFS = [
        FieldDef(title='hash', allowed_types=[unicode]),
        FieldDef(title='url', allowed_types=[unicode]),
        FieldDef(title='file', allowed_types=[{unicode: file}], validate=False),
    ]

    CREATE_ONLY = ['file']


class AdUser(FacebookModel):

    """
    Represents the aduser object in the Facebook Ads API:
    https://developers.facebook.com/docs/reference/ads-api/aduser/

    """
    FIELD_DEFS = [
        FieldDef(title='id', allowed_types=[long]),
        FieldDef(title='permissions', allowed_types=[[int]]),
        FieldDef(title='role', allowed_types=[int], choices=[1001, 1002, 1003]),
    ]

    CREATE_ONLY = ['role']


class AdStatistic(FacebookModel):

    """
    Represents an adstatistic objects in the Facebook Ads API:
    https://developers.facebook.com/docs/reference/ads-api/adstatistics

    """
    FIELD_DEFS = [
        FieldDef(title='id', allowed_types=[unicode]),
        FieldDef(title='account_id', allowed_types=[long]),
        FieldDef(title='adcampaign_id', allowed_types=[long]),
        FieldDef(title='adgroup_id', allowed_types=[long]),
        FieldDef(title='impressions', allowed_types=[int]),
        FieldDef(title='clicks', allowed_types=[int]),
        FieldDef(title='spent', allowed_types=[int]),
        FieldDef(title='social_impressions', allowed_types=[int]),
        FieldDef(title='social_clicks', allowed_types=[int]),
        FieldDef(title='social_spent', allowed_types=[int]),
        FieldDef(title='unique_impressions', allowed_types=[int]),
        FieldDef(title='unique_clicks', allowed_types=[int]),
        FieldDef(title='social_unique_impressions', allowed_types=[int]),
        FieldDef(title='social_unique_clicks', allowed_types=[int]),
        FieldDef(title='start_time', allowed_types=[datetime.datetime, type(None)]),
        FieldDef(title='end_time', allowed_types=[datetime.datetime, type(None)]),
    ]


class BroadTargetingCategory(SupportModel):

    """
    Represents the broadtargetingcategory object in the Facebook Ads API:
    https://developers.facebook.com/docs/reference/ads-api/targeting-specs/

    """
    FIELD_DEFS = [
        FieldDef(title='id', allowed_types=[long]),
        FieldDef(title='name', allowed_types=[unicode]),
        FieldDef(title='parent_category', allowed_types=[unicode, type(None)]),
        FieldDef(title='size', allowed_types=[int]),
        FieldDef(title='type', allowed_types=[int]),
        FieldDef(title='type_name', allowed_types=[unicode]),
    ]


class Region(SupportModel):

    """
    Represents a region for ad targeting purposes. See documentation:
    https://developers.facebook.com/docs/reference/ads-api/targeting-specs/

    """
    FIELD_DEFS = [
        FieldDef(title='id', allowed_types=[unicode]),
        FieldDef(title='name', allowed_types=[unicode]),
    ]


class Country(SupportModel):

    """
    Represents a country for ad targeting purposes. See documentation:
    https://developers.facebook.com/docs/reference/ads-api/targeting-specs/

    """
    FIELD_DEFS = [
        FieldDef(title='country_code', allowed_types=[unicode]),
        FieldDef(title='name', allowed_types=[unicode]),
        FieldDef(title='supports_region', allowed_types=[bool]),
        FieldDef(title='supports_city', allowed_types=[bool]),
    ]


class City(SupportModel):

    """
    Represents a city for ad targeting purposes. See documentation:
    https://developers.facebook.com/docs/reference/ads-api/targeting-specs/

    """
    FIELD_DEFS = [
        FieldDef(title='id', allowed_types=[unicode]),
        FieldDef(title='name', allowed_types=[unicode]),
    ]


class CollegeNetwork(SupportModel):

    """
    Represents a college network for ad targeting purposes. See documentation:
    https://developers.facebook.com/docs/reference/ads-api/targeting-specs/

    """
    FIELD_DEFS = [
        FieldDef(title='id', allowed_types=[unicode]),
        FieldDef(title='name', allowed_types=[unicode]),
    ]


class WorkNetwork(SupportModel):

    """
    Represents a work network for ad targeting purposes. See documentation:
    https://developers.facebook.com/docs/reference/ads-api/targeting-specs/

    """
    FIELD_DEFS = [
        FieldDef(title='id', allowed_types=[unicode]),
        FieldDef(title='name', allowed_types=[unicode]),
    ]


class UserConnection(SupportModel):
    FIELD_DEFS = [
        FieldDef(title='id', allowed_types=[unicode]),
        FieldDef(title='name', allowed_types=[unicode]),
    ]


class Targeting(SupportModel):

    """
    Represents a targeting object in the Facebook Ads API:
    https://developers.facebook.com/docs/reference/ads-api/targeting-specs/

    """
    FIELD_DEFS = [
        FieldDef(title='genders', allowed_types=[[int]], choices=[[1], [2], [1, 2]]),
        FieldDef(title='age_min', allowed_types=[int]),
        FieldDef(title='age_max', allowed_types=[int]),
        FieldDef(title='broad_age', allowed_types=[int], choices=[0, 1]),
        FieldDef(title='countries', allowed_types=[[unicode]]),
        FieldDef(title='cities', allowed_types=[[City]]),
        FieldDef(title='regions', allowed_types=[[Region]]),
        FieldDef(title='radius', allowed_types=[int]),
        FieldDef(title='conjunctive_user_adclusters', allowed_types=[[BroadTargetingCategory]]),
        FieldDef(title='excluded_user_adclusters', allowed_types=[[BroadTargetingCategory]]),
        FieldDef(title='keywords', allowed_types=[[unicode]]),
        FieldDef(title='user_os', allowed_types=[[unicode]]),
        FieldDef(title='user_device', allowed_types=[[unicode]], choices=['iPhone', 'iPod', 'android_tablet', 'android_smartphone']),
        FieldDef(title='wireless_carrier', allowed_types=[[unicode]], choices=['WiFi']),
        FieldDef(title='site_category', allowed_types=[[unicode]], choices=['feature_phones']),
        FieldDef(title='connections', allowed_types=[[UserConnection]]),
        FieldDef(title='excluded_connections', allowed_types=[[UserConnection]]),
        FieldDef(title='friends_of_connections', allowed_types=[[UserConnection]]),
        FieldDef(title='college_networks', allowed_types=[[CollegeNetwork]]),
        FieldDef(title='work_networks', allowed_types=[[WorkNetwork]]),
        FieldDef(title='education_statuses', allowed_types=[[int]], choices=[[1], [2], [3]]),
        FieldDef(title='college_majors', allowed_types=[[unicode]]),
        FieldDef(title='page_types', allowed_types=[[unicode]], choices=[['desktop'], ['feed'], ['desktopfeed'], ['mobile'], ['rightcolumn'], ['home']]),
        FieldDef(title='relationship_statuses', allowed_types=[[int]]),
        FieldDef(title='interested_in', allowed_types=[[int]], choices=[[1], [2]]),
        FieldDef(title='locales', allowed_types=[{unicode: unicode, unicode:unicode}, [unicode]]),
    ]


class ActionSpec(SupportModel):

    """
    Represents the actionspec object in the Facebook Ads API:
    https://developers.facebook.com/docs/reference/ads-api/action-specs/

    Currently this supports ONLY on-site objects and actions

    """
    FIELD_DEFS = [
        FieldDef(title='action.type', allowed_types=[[unicode]]),
        FieldDef(title='applicaton', allowed_types=[[long]]),
        FieldDef(title='offer', allowed_types=[[long]]),
        FieldDef(title='event', allowed_types=[[long]]),
        FieldDef(title='question', allowed_types=[[long]]),
        FieldDef(title='page', allowed_types=[[long]]),
        FieldDef(title='post', allowed_types=[[long]]),
    ]


class TrackingSpec(SupportModel):

    """
    Represents the trackingspec object in the Facebook Ads API:
    https://developers.facebook.com/docs/reference/ads-api/tracking-specs

    """
    FIELD_DEFS = [
        FieldDef(title='action.type', allowed_types=[[unicode]]),
        FieldDef(title='page', allowed_types=[[long]]),
        FieldDef(title='application', allowed_types=[[long]]),
        FieldDef(title='object', allowed_types=[[unicode]]),
        FieldDef(title='object.domain', allowed_types=[[unicode]]),
        FieldDef(title='post', allowed_types=[[long]]),
        FieldDef(title='post.wall', allowed_types=[[long]]),
        FieldDef(title='offer', allowed_types=[[long]]),
    ]


class AdPreviewCss(FacebookModel):

    """
    Represents the AdPreview Css object in the Facebook Ads API:
    https://developers.facebook.com/docs/reference/ads-api/generatepreview/#adpreviewcss
    """
    FIELD_DEFS = [
        FieldDef(title='result', allowed_types=[unicode]),
    ]


class Preview(FacebookModel):

    """
    Represents the Preview object in the Facebook Ads API:
    https://developers.facebook.com/docs/reference/ads-api/generatepreview/
    """
    FIELD_DEFS = [
        FieldDef(title='body', allowed_types=[unicode]),
    ]

NewFieldDef = namedtuple('NewFieldDef', ['title', 'allowed_types', 'choices'])


class AdBase(object):
    """
    Common class for AdAccount, AdCampaign, AdCreative, AdGroup to simulate TinyModel.
    """
    def __repr__(self):
        frepr = {}
        for x in self.FIELDS:
            frepr[x['field_def'].title] = x['value']
        return str(self.__class__) + "\nFIELDS:\n" + str(frepr) + "\n"

    def __getattr__(self, name):
        fields = object.__getattribute__(self, 'FIELDS')
        f = next((x for x in fields if x['field_def'].title == name), None)
        if f:
            return f['value']
        else:
            raise AttributeError(str(self.__class__) + " has no field " + name)

    def __setattr__(self, key, value):
        field_def = next((x for x in self.FIELD_DEFS if x.title == key), False)
        if field_def:
            if type(value) in [str, unicode, int, long] and datetime.datetime in field_def.allowed_types:
                if type(value) in [int, long]:
                    value = datetime.datetime.fromtimestamp(value)
                elif type(value) in [str, unicode]:
                    value = date_parser.parser(value)
                else:
                    raise ValueError
            if self.__validate(value, field_def.allowed_types):
                if 'choices' in field_def:
                    if self.__checkchoices(value, field_def.choices):
                        self.__add_field(field_def, value)
                    else:
                        e = "{0} is not present in choices {1}".format(value, field_def.choices)
                        raise ValueError(e)
                else:
                    self.__add_field(field_def, value)
            else:
                e = "{0} does not validate against allowed_types {1}"\
                    .format(value, field_def.allowed_types)
                raise ValueError(e)

    def __init__(self, from_json=False, **kwargs):
        object.__setattr__(self, 'FIELDS', [])
        if from_json:
            initial_attrib = self.__from_json(from_json)
        else:
            initial_attrib = kwargs

        for (key, value) in initial_attrib.items():
            setattr(self, key, value)

    def __from_json(self, json_data):
        return json.loads(json_data)

    def __checkchoices(self, value, choices):
        if value in choices:
            return True

    def __add_field(self, field_def, value):
        this_field = next((x for x in self.FIELDS if x['field_def'].title == field_def.title), None)
        if not this_field:
            self.FIELDS.append({'field_def': field_def, 'value': value})
        else:
            this_field['value'] = value

    def __validate(self, value, allowed_types):

        if long in allowed_types:
            allowed_types.append(int)

        if isinstance(value, str):
            value = unicode(value)

        if isinstance(value, dict):
            new_val = {}
            for k, v in value.iteritems():
                if type(k) == str:
                    k = unicode(k)
                elif type(v) == str:
                    v = unicode(v)
                new_val[k] = v
            dict_validator = [x for x in allowed_types if type(x) == dict][0]
            key_type = dict_validator.keys()[0]
            val_type = dict_validator.values()[0]
            if key_type == type(new_val.keys()[0]) and val_type == type(new_val.values()[0]):
                return True

        if isinstance(allowed_types, list):
            if len(allowed_types) > 1:
                if type(value) in tuple(allowed_types):
                    return True
            else:
                if not isinstance(allowed_types[0], list):
                    if isinstance(value, allowed_types[0]):
                        return True
                else:
                    whole_list_validator = []
                    for v in value:
                        if isinstance(v, allowed_types[0][0]):
                            whole_list_validator.append(True)
                        else:
                            whole_list_validator.append(False)
                    if True in whole_list_validator:
                        return True


class AdCreative(AdBase):

    """
    Represents the adcreative object in the Facebook Ads API:
    https://developers.facebook.com/docs/reference/ads-api/adcreative

    """
    FIELD_DEFS = (
        NewFieldDef(title='id', allowed_types=[long], choices=None),
        NewFieldDef(title='type', allowed_types=[int], choices=[1, 2, 3, 4, 12, 25, 27]),
        NewFieldDef(title='object_id', allowed_types=[long], choices=None),
        NewFieldDef(title='name', allowed_types=[unicode], choices=None),
        NewFieldDef(title='title', allowed_types=[unicode], choices=None),
        NewFieldDef(title='body', allowed_types=[unicode], choices=None),
        NewFieldDef(title='image_hash', allowed_types=[unicode, type(None)], choices=None),
        NewFieldDef(title='image_url', allowed_types=[unicode], choices=None),
        NewFieldDef(title='link_url', allowed_types=[unicode], choices=None),
        NewFieldDef(title='preview_url', allowed_types=[unicode], choices=None),
        NewFieldDef(title='url_tags', allowed_types=[unicode], choices=None),
        NewFieldDef(title='related_fan_page', allowed_types=[long], choices=None),
        NewFieldDef(title='story_id', allowed_types=[long], choices=None),
        NewFieldDef(title='follow_redirect', allowed_types=[bool], choices=None),
        NewFieldDef(title='auto_update', allowed_types=[bool], choices=None),
        NewFieldDef(title='action_spec', allowed_types=[[ActionSpec]], choices=None),
        NewFieldDef(title='previews', allowed_types=[[Preview]], choices=None),
    )

    def __init__(self, from_json=False, **kwargs):
        super(AdCreative, self).__init__(from_json, **kwargs)


class AdGroup(AdBase):

    """
    Represents an adgroup object in the Facebook Ads API:
    https://developers.facebook.com/docs/reference/ads-api/adgroup

    """
    FIELD_DEFS = (
        NewFieldDef(title='id', allowed_types=[long], choices=None),
        NewFieldDef(title='name', allowed_types=[unicode], choices=None),
        NewFieldDef(title='account_id', allowed_types=[int], choices=None),
        NewFieldDef(title='campaign_id', allowed_types=[long], choices=None),
        NewFieldDef(title='adgroup_status', allowed_types=[unicode],
                    choices=['ACTIVE', 'DELETED', 'PENDING_REVIEW', 'DISAPPROVED',
                             'PENDING_BILLING_INFO', 'CAMPAIGN_PAUSED', 'ADGROUP_PAUSED']),
        NewFieldDef(title='disapprove_reason_descriptions', allowed_types=[unicode], choices=None),
        NewFieldDef(title='bid_type', allowed_types=[unicode],
                    choices=['CPC', 'CPM', 'MULTI_PREMIUM', 'RELATIVE_OCPM', 'ABSOLUTE_OCPM', 'CPA']),
        NewFieldDef(title='bid_info', allowed_types=[{unicode: int}, type(None)], choices=None),
        NewFieldDef(title='creative_ids', allowed_types=[[long]], choices=None),
        NewFieldDef(title='creative', allowed_types=[{unicode: long}], choices=None),
        NewFieldDef(title='targeting', allowed_types=[Targeting, type(None)], choices=None),
        NewFieldDef(title='tracking_specs', allowed_types=[[TrackingSpec]], choices=None),
        NewFieldDef(title='last_updated_by_app_id', allowed_types=[long], choices=None),
        NewFieldDef(title='created_time', allowed_types=[datetime.datetime], choices=None),
        NewFieldDef(title='updated_time', allowed_types=[datetime.datetime], choices=None),
        NewFieldDef(title='stats', allowed_types=[[AdStatistic]], choices=None),
        NewFieldDef(title='adcreatives', allowed_types=[[AdCreative]], choices=None),
        NewFieldDef(title='previews', allowed_types=[[Preview]], choices=None),
    )

    def __init__(self, from_json=False, **kwargs):
        super(AdGroup, self).__init__(from_json, **kwargs)


class AdCampaign(AdBase):

    """
    Represents the aduser object in the Facebook Ads API:
    https://developers.facebook.com/docs/reference/ads-api/adcampaign/

    """
    FIELD_DEFS = (
        NewFieldDef(title='id', allowed_types=[long], choices=None),
        NewFieldDef(title='name', allowed_types=[unicode], choices=None),
        NewFieldDef(title='account_id', allowed_types=[long], choices=None),
        NewFieldDef(title='start_time', allowed_types=[datetime.datetime], choices=None),
        NewFieldDef(title='end_time', allowed_types=[datetime.datetime], choices=None),
        NewFieldDef(title='created_time', allowed_types=[datetime.datetime], choices=None),
        NewFieldDef(title='updated_time', allowed_types=[datetime.datetime], choices=None),
        NewFieldDef(title='daily_budget', allowed_types=[int], choices=None),
        NewFieldDef(title='lifetime_budget', allowed_types=[int], choices=None),
        NewFieldDef(title='budget_remaining', allowed_types=[int], choices=None),
        NewFieldDef(title='campaign_status', allowed_types=[int], choices=[1, 2, 3]),
        NewFieldDef(title='adcreatives', allowed_types=[[AdCreative]], choices=None),
        NewFieldDef(title='adgroups', allowed_types=[[AdGroup]], choices=None),
        NewFieldDef(title='stats', allowed_types=[[AdStatistic]], choices=None),
    )

    def __init__(self, from_json=False, **kwargs):
        super(AdCampaign, self).__init__(from_json, **kwargs)


class AdAccount(AdBase):
    """
    Represents the adaccount object in the Facebook Ads API:
    https://developers.facebook.com/docs/reference/ads-api/adaccount/

    """
    FIELD_DEFS = (
        NewFieldDef(title='id', allowed_types=[unicode], choices=None),
        NewFieldDef(title='account_id', allowed_types=[long], choices=None),
        NewFieldDef(title='name', allowed_types=[unicode], choices=None),
        NewFieldDef(title='account_status', allowed_types=[int], choices=None),
        NewFieldDef(title='currency', allowed_types=[unicode], choices=None),
        NewFieldDef(title='timezone_id', allowed_types=[int], choices=None),
        NewFieldDef(title='timezone_name', allowed_types=[unicode], choices=None),
        NewFieldDef(title='timezone_offset_hours_utc', allowed_types=[int], choices=None),
        NewFieldDef(title='vat_status', allowed_types=[int], choices=None),
        NewFieldDef(title='daily_spend_limit', allowed_types=[int], choices=None),
        NewFieldDef(title='amount_spent', allowed_types=[int], choices=None),
        NewFieldDef(title='users', allowed_types=[[AdUser]], choices=None),
        NewFieldDef(title='adcampaigns', allowed_types=[[AdCampaign]], choices=None),
        NewFieldDef(title='adimages', allowed_types=[[AdImage]], choices=None),
        NewFieldDef(title='adcreatives', allowed_types=[[AdCreative]], choices=None),
        NewFieldDef(title='adgroups', allowed_types=[[AdGroup]], choices=None),
        NewFieldDef(title='stats', allowed_types=[[AdStatistic]], choices=None),
        NewFieldDef(title='adgroupstats', allowed_types=[[AdStatistic]], choices=None),
        NewFieldDef(title='adpreviewscss', allowed_types=[[AdPreviewCss]], choices=None),
    )

    def __init__(self, from_json=False, **kwargs):
        super(AdAccount, self).__init__(from_json, **kwargs)


class Post(FacebookModel):
    FIELD_DEFS = [
        FieldDef(title='id', allowed_types=[unicode]),
        FieldDef(title='message', allowed_types=[unicode]),
        FieldDef(title='picture', allowed_types=[unicode, type(None)]),
        FieldDef(title='link', allowed_types=[unicode, type(None)]),
        FieldDef(title='published', allowed_types=[bool]),
    ]
