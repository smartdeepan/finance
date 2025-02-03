import re

def generate_index_urls(fund_names):
    """
    Generates a dictionary of invested indices and their URLs.

    This function takes a list of fund names and returns a dictionary where keys are fund names
    and values are the corresponding Nifty index URLs. It handles various naming conventions
    and URL structures used by Nifty Indices.

    Args:
        fund_names (list): A list of strings, where each string is the name of a fund.

    Returns:
        dict: A dictionary where keys are fund names and values are the corresponding Nifty index URLs.
              Returns an empty dictionary if no matching URLs are found for any fund.
    """

    base_url = "https://www.niftyindices.com/IndexConstituent/ind_nifty"
    base_url_index_constituent = "https://www.niftyindices.com/IndexConstituent/"

    nifty_indices = {
        "Bandhan Nifty Alpha 50 Index Fund Direct Growth": r"ind_nifty_Alpha_Index",
        "Edelweiss Nifty Large Mid Cap 250 Index Fund Direct Growth": r"niftylargemidcap250",
        "Mirae Asset Nifty MidSmallcap400 Momentum Quality 100 ETF FoF Dir Growth":
            r"niftymidsmallcap400momentumquality100",
        "Mirae Asset Nifty Smallcap 250 Momentum Quality 100 ETF FoF Dir Growth":
            r"niftysmallcap250momentumquality100",
        "Mirae Asset Nifty200 Alpha 30 ETF Fund of Fund Direct Growth": r"nifty200alpha30",
        "Motilal Oswal Nifty 200 Momentum 30 Index Fund Direct Growth": r"nifty200momentum30",
        "Motilal Oswal Nifty India Defence Index Fund Direct Growth": r"ind_niftyindiadefence_list",
        "Nippon India Nifty 50 Value 20 Index Fund Direct Growth": r"nifty50value20",
        "Nippon India Nifty 500 Momentum 50 Index Fund Direct Growth": r"nifty500momentum50",
        "Parag Parikh Flexi Cap Direct Growth": None,  # Not a Nifty index fund
        "Quant Flexi Cap Fund Direct Growth": None,  # Not a Nifty index fund
        "Tata Nifty Midcap 150 Momentum 50 Index Fund Direct Growth": r"ind_niftymidcap150momentum50_list",
        "Tata Nifty Realty Index Fund Direct Growth": r"niftyrealty",
        "UTI Nifty 500 Value 50 Index Fund Direct Growth": r"nifty500value50",
    }

    invested_indices_urls = {}

    for fund_name in fund_names:
        pattern = nifty_indices.get(fund_name)
        if pattern:
            # Enhanced regex to capture various Nifty index name formats
            match = re.search(r"nifty(\d+|next\d+|bank|it|midcap100|largemidcap250|smallcap100|200|500|alpha50|large mid cap 250|midsmallcap400|smallcap250|50 value 20|500 momentum 50|midcap 150|realty|500 value 50|200 momentum 30|200 alpha 30|smallcap 250 momentum quality 100|midsmallcap400 momentum quality 100)", pattern, re.IGNORECASE)  # Added re.IGNORECASE
            if match:
                index_name = match.group(1).replace(" ", "")  # Remove spaces from index name
                url = base_url + index_name + "list.csv"
                invested_indices_urls[fund_name] = url
            elif pattern:  # Handle cases where the pattern is not in the first format
                url = base_url_index_constituent + pattern + ".csv"
                invested_indices_urls[fund_name] = url
        else:
            print(f"No Nifty index information found for fund: {fund_name}")  # Informative message

    return invested_indices_urls


def get_invested_indices_urls():
    """Returns the dictionary of invested indices and their URLs."""
    # Enter the fund names where you have invested.
    fund_names = [
        "Motilal Oswal Nifty India Defence Index Fund Direct Growth",
        "Bandhan Nifty Alpha 50 Index Fund Direct Growth",
        "Edelweiss Nifty Large Mid Cap 250 Index Fund Direct Growth",
        "Mirae Asset Nifty MidSmallcap400 Momentum Quality 100 ETF FoF Dir Growth",
        "Mirae Asset Nifty Smallcap 250 Momentum Quality 100 ETF FoF Dir Growth",
        "Mirae Asset Nifty200 Alpha 30 ETF Fund of Fund Direct Growth",
        "Motilal Oswal Nifty 200 Momentum 30 Index Fund Direct Growth",
        "Nippon India Nifty 50 Value 20 Index Fund Direct Growth",
        "Nippon India Nifty 500 Momentum 50 Index Fund Direct Growth",
        "Parag Parikh Flexi Cap Direct Growth",
        "Quant Flexi Cap Fund Direct Growth",
        "Tata Nifty Midcap 150 Momentum 50 Index Fund Direct Growth",
        "Tata Nifty Realty Index Fund Direct Growth",
        "UTI Nifty 500 Value 50 Index Fund Direct Growth",
    ]
    return generate_index_urls(fund_names)  # Call the function to generate and return the URLs


# Example usage (you can remove this if you're using this as a module)
if __name__ == "__main__":
    invested_indices_urls = get_invested_indices_urls()
    print(invested_indices_urls)