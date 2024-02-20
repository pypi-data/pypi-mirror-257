from enum import Enum


class ChangeType(Enum):
    ADD_FEATURE_CHANGE = 'AddFeatureChange'
    DISCONTINUOUS_LOCATION_END_CHANGE = 'DiscontinuousLocationEndChange'
    DISCONTINUOUS_LOCATION_START_CHANGE = 'DiscontinuousLocationStartChange'
    FEATURE_ATTRIBUTE_CHANGE = 'FeatureAttributeChange'
    LOCATION_END_CHANGE = 'LocationEndChange'
    LOCATION_START_CHANGE = 'LocationStartChange'
    DELETE_FEATURE_CHANGE = 'DeleteFeatureChange'

