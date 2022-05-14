from data.constants import calories_for_product


def calculate_calories_for_product(product: str, gram: int):
    product = product.lower()
    if product in calories_for_product:
        return int(calories_for_product[product] / 100 * gram)

    search_result = [value for key, value in calories_for_product.items() if product in key]
    if search_result:
        return int((sum(search_result) / len(search_result)) / 100 * gram)
