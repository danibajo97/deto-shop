import re


def total_price(total, quantity, cart_items):
    for rs in cart_items:
        if rs.variations.discount_price:
            total += round((rs.variations.discount_price * rs.quantity), 2)
            quantity += rs.quantity
        else:
            total += round((rs.variations.price * rs.quantity), 2)
            quantity += rs.quantity
    grand_total = round(total, 2)
    return grand_total


def total_item(cart_items):
    cart_count = 0
    for item in cart_items:
        cart_count += item.quantity
    return cart_count


def max_min_values(filter):
    numbers = [float(s) for s in re.findall(r'-?\d+\.?\d*', filter)]
    min = numbers[0]
    max = numbers[1]
    return max, min


def filter_price_products(variations, max, min):
    min_price_variations = []
    max_price_variations = []
    final_list = []

    for v_item in variations:
        if v_item.discount_price is not None and v_item.discount_price >= min:
            min_price_variations.append(v_item)
        elif v_item.price >= min:
            min_price_variations.append(v_item)

    for v_item in variations:
        if v_item.discount_price is not None and v_item.discount_price <= max:
            max_price_variations.append(v_item)
        elif v_item.price <= max:
            max_price_variations.append(v_item)

    for item in min_price_variations:
        if (item not in final_list) and (
                item in max_price_variations):
            final_list.append(item)

    return final_list


def find_colors(variations, colors):
    color_final_result = []
    for item in variations:
        for color in colors:
            if item.color is not None and item.color.id == int(color) and item is not color_final_result:
                color_final_result.append(item)
    return color_final_result


def find_sizes(variations, sizes):
    sizes_final_result = []
    for item in variations:
        for size in sizes:
            if item.size is not None and item.size.id == int(size) and item is not sizes_final_result:
                sizes_final_result.append(item)
    return sizes_final_result

