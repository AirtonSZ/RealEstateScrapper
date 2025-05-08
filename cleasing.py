def get_text_between(text, start_str, end_str):
    """
    Gets the text between two strings.

    Parameters
    ----------
    text : str
        The text to search.
    start_str : str
        The starting string. If None, the text is returned.
    end_str : str
        The ending string. If None, the text is returned.

    Returns
    -------
    str
        The text between the two strings.
    """
    if start_str == None and end_str == None:
        return text
    
    start = 0
    offset = 0
    if start_str != None and text.find(start_str) != -1:
        start = text.find(start_str)
        offset = len(start_str)

    if end_str != None and text.find(end_str) != -1:
        end = text.find(end_str)
        return text[start+offset:end]

    return text[start+offset:]

def clean_price(text):
    """
    Cleans a price string by removing spaces, the 'R$' currency symbol, decimal points, and unwanted strings.
    
    Parameters
    ----------
    text : str
        The string to clean.
    
    Returns
    -------
    str
        The cleaned string.
    """
    text=text.replace(' ','')
    text=text.replace('R$','').replace('\.','')
    text=text.replace('Apartirde','').replace('apartirde','')
    text=text.replace('Valorsobconsulta','-')