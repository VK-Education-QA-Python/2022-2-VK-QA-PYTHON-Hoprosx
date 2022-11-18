campaign_data = data = {
    "name": "",
    "read_only": False,
    "conversion_funnel_id": None,
    "objective": "special",
    "targetings": {
        "sex": ["male", "female"],
        "age": {"age_list": [75], "expand": True},
        "pads": [784699, 784700],
    },
    "age_restrictions": None,
    "date_start": None,
    "date_end": None,
    "budget_limit_day": "600",
    "budget_limit": "1000",
    "mixing": "recommended",
    "price": "0.01",
    "max_price": "0",
    "package_id": 2266,  # задается автоматически при выборе кампании с типом "специальные возможности"
    "banners": [
        {
            "textblocks": {"billboard_video": {"text": "Hello World"}},
            "urls": {"primary": {"id": ""}},
            "name": "",
        }
    ],
}

segment_segment_apps_and_games_in_social_media_data = {
    "name": "",
    "pass_condition": 1,
    "relations": [
        {
            "object_type": "remarketing_player",
            "params": {"type": "positive", "left": 365, "right": 0},
        }
    ],
    "logicType": "or",
}

segment_groups_OK_and_VK_data = {
    "name": "",
    "pass_condition": 1,
    "relations": [
        {
            "object_type": "remarketing_group",
            "params": {
                "source_id": "",
                "source_type": "group",
                "type": "positive"
            }
        }
    ],
    "logicType": "or"
}
