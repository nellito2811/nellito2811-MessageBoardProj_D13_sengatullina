# from django.template.defaulttags import register

# def adv_plural(advertisement_count):
#     if advertisement_count == 0:
#         return str(advertisement_count) + ' объявлений'
#     if advertisement_count == 1:
#         return str(advertisement_count) + ' объявление'
#     if advertisement_count >= 11 and advertisement_count >= 11:
#         return str(advertisement_count) + ' объявлений'     
#     if advertisement_count % 10 == 1:
#         return str(advertisement_count) + ' объявление'
#     if advertisement_count > 1 and advertisement_count < 5:
#         return str(advertisement_count) + ' объявления'
#     if advertisement_count % 10 > 1 and advertisement_count % 10 < 5:
#         return str(advertisement_count) + ' объявления'    
#     if advertisement_count  > 4 and advertisement_count <= 20:
#         return str(advertisement_count) + ' объявлений'
#     if advertisement_count % 10 == 0:
#         return str(advertisement_count) + ' объявлений'
#     if advertisement_count % 10  > 4 and advertisement_count % 10 <= 20:
#         return str(advertisement_count) + ' объявлений'
#     return str(advertisement_count) 

# def test_adv_plur (count):
#     for i in range(count):
#         print(adv_plural(i))
    
    
# def adv_plural_2(advertisement_count):
#     adv_str = str(advertisement_count)
#     adv_ending = int(str(advertisement_count)[-1])
#     adv_ending_2 = int(str(advertisement_count)[-2:])
#     if len(adv_str)>=2 and adv_ending_2 >= 11 and adv_ending_2 <= 14:
#         return str(advertisement_count) + " объявлений"
#     if adv_ending == 1:
#         return str(advertisement_count) + " объявление"
#     if adv_ending == 2 or adv_ending == 3 or adv_ending == 4:
#         return str(advertisement_count) + " объявления"
#     if adv_ending == 5 or adv_ending == 6 or adv_ending == 7 or adv_ending == 8 or adv_ending == 9 or adv_ending == 0:
#         return str(advertisement_count) + " объявлений"
    

# def test_adv_plur_2 (count):
#     for i in range(count):
#         print(adv_plural_2(i))



def adv_plural_2(advertisement_count):
    adv_str = str(advertisement_count)
    adv_ending = int(adv_str[-1])

    if len(adv_str) >= 2 and (int (adv_str[-2:]) >= 11 and int (adv_str[-2:]) <=14):
        return str(advertisement_count) + " объявлений"
    if adv_ending == 1:
        return str(advertisement_count) + " объявление"
    if adv_ending == 2 or adv_ending == 3 or adv_ending == 4:
        return str(advertisement_count) + " объявления"
    if adv_ending == 5 or adv_ending == 6 or adv_ending == 7 or adv_ending == 8 or adv_ending == 9 or adv_ending == 0:
        return str(advertisement_count) + " объявлений"


# @register.filter
# def in_field(query, field_name):
#     return query.values_list(field_name, flat=True)