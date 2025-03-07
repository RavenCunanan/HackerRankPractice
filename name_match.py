def name_match(aliases, record_name):
    """
    Check if the record_name matches any name in the list of aliases.

    :param aliases: List of known aliases (strings)
    :param record_name: Name returned on a record (string)
    :return: 1 if a match is found, otherwise 0
    """
    def extract_first_last(name):
        parts = name.split()
        return parts[0], parts[-1]  # First and last name only
    
    record_first, record_last = extract_first_last(record_name)
    
    for alias in aliases:
        alias_first, alias_last = extract_first_last(alias)
        # Match if first and last names are the same, ignoring middle name differences
        if record_first == alias_first and record_last == alias_last:
            return 1  

    return 0

# Example usage:
aliases = ["Alphonse Gabriel Capone", "Alphonse F Capone", "Alphonse Francis Capone"]
record_name = "Alphonse Capone"
print(name_match(aliases, record_name))  # Expected Output: 1
