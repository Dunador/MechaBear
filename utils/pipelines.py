profile_pipeline = [
    {
        '$lookup': {
            'from': 'MainQuest',
            'localField': 'member_id',
            'foreignField': 'member_id',
            'as': 'MainQuest'
        }
    }, {
        '$lookup': {
            'from': 'characters',
            'localField': 'member_id',
            'foreignField': 'member_id',
            'as': 'characters'
        }
    }, {
        '$lookup': {
            'from': 'guilds',
            'localField': 'member_id',
            'foreignField': 'member_id',
            'as': 'guilds'
        }
    }, {
        '$lookup': {
            'from': 'points',
            'localField': 'member_id',
            'foreignField': 'member_id',
            'as': 'points'
        }
    }, {
        '$lookup': {
            'from': 'tokens',
            'localField': 'member_id',
            'foreignField': 'member_id',
            'as': 'tokens'
        }
    }, {
        '$lookup': {
            'from': 'trophies',
            'localField': 'member_id',
            'foreignField': 'member_id',
            'as': 'trophies'
        }
    }, {
        '$unwind': {
            'path': '$MainQuest'
        }
    }, {
        '$unwind': {
            'path': '$characters'
        }
    }, {
        '$unwind': {
            'path': '$guilds'
        }
    }, {
        '$project': {
            '_id': 0,
            'MainQuest': '$MainQuest.MainQuest',
            'guilds': '$guilds.guilds',
            'trophies': {
                '$arrayElemAt': [
                    '$trophies.trophies', 0
                ]
            },
            'characters': '$characters.characters',
            'points': {
                '$arrayElemAt': [
                    '$points.points', 0
                ]
            },
            'tokens': {
                '$arrayElemAt': [
                    '$tokens.tokens', 0
                ]
            }
        }
    }
]

