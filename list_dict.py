def convert_to_dict_list(data):
    result = []
    count=0
    for item in data:
        dict_item = {
            'id': count,
            'messin_date': item[1].strftime('%Y-%m-%d'),
            'messout_date': item[2].strftime('%Y-%m-%d'),
            'days': item[3]
        }
        count=count+1
        
        result.append(dict_item)
    return result